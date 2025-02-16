from datetime import timedelta
from api.services.jwt import JwtService
from api.main import get_runtime_settings
from shared.entities.email_verification import EmailVerificationRepository
from shared.entities.refresh_token import RefreshTokenRepository
from shared.entities.user.repo import UserRepository
from shared.settings import Settings
from shared.utils import utc_now, validate_password
from .models import TokenSet, VerificationRequestId


class AuthService:
    class UserNotFound(Exception): ...

    class InvalidPassword(Exception): ...

    class UsernameExists(Exception): ...

    class EmailExists(Exception): ...

    class InvalidRefreshToken(Exception): ...

    class InvalidRequestId(Exception): ...

    class InvalidCode(Exception): ...

    def __init__(
        self,
        user_repo: UserRepository,
        refresh_token_repo: RefreshTokenRepository,
        email_verification_repo: EmailVerificationRepository,
        jwt_service: JwtService,
        settings: Settings,
    ):
        super().__init__()
        self.user_repo = user_repo
        self.refresh_token_repo = refresh_token_repo
        self.email_verification_repo = email_verification_repo
        self.jwt_service = jwt_service
        self.settings = settings

    async def _generate_complete_jwt_set(self, user_id: int) -> TokenSet:
        jwt = self.jwt_service.new(user_id)
        refresh = self.refresh_token_repo.new(user_id)
        await self.refresh_token_repo.save(refresh)
        return TokenSet(
            access_token=jwt,
            refresh_token=str(refresh.id),
            access_token_expires_in=self.settings.access_token_expires_in,
            refresh_token_expires_in=self.settings.refresh_token_expires_in,
        )

    async def login(self, email: str, password: str) -> TokenSet:
        user = await self.user_repo.find_by_email(email)
        if user is None:
            raise AuthService.UserNotFound()
        if not validate_password(user.password_hash, password):
            raise AuthService.InvalidPassword
        return await self._generate_complete_jwt_set(user.id)

    if get_runtime_settings().email_verification_enabled:

        async def register(  # type: ignore
            self, email: str, username: str, password: str
        ) -> VerificationRequestId:
            match await self.user_repo.lookup_by_email_or_username(email, username):
                case "email":
                    raise AuthService.EmailExists
                case "username":
                    raise AuthService.UsernameExists
            raise NotImplementedError

    else:

        async def register(self, email: str, username: str, password: str) -> TokenSet:
            match await self.user_repo.lookup_by_email_or_username(email, username):
                case "email":
                    raise AuthService.EmailExists
                case "username":
                    raise AuthService.UsernameExists
            user = self.user_repo.new(email, username, password, True)
            await self.user_repo.save(user)
            return await self._generate_complete_jwt_set(user.id)

    async def refresh(self, refresh_token: str) -> TokenSet:
        token = await self.refresh_token_repo.find(refresh_token)
        if token is None:
            raise AuthService.InvalidRefreshToken
        await self.refresh_token_repo.delete(str(token.id))
        if (
            token.created_at + timedelta(seconds=self.settings.refresh_token_expires_in)
        ) < utc_now():
            raise AuthService.InvalidRefreshToken
        return await self._generate_complete_jwt_set(token.user_id)

    async def verify(self, request_id: str, code: str) -> TokenSet:
        verify = await self.email_verification_repo.find(request_id)
        if verify is None:
            raise AuthService.InvalidRequestId
        if verify.code != code:
            raise AuthService.InvalidCode
        await self.email_verification_repo.delete(request_id)
        await self.user_repo.enable(verify.user_id)
        return await self._generate_complete_jwt_set(verify.user_id)

    async def logout(self, refresh_token_id: str) -> None:
        await self.refresh_token_repo.delete(refresh_token_id)
