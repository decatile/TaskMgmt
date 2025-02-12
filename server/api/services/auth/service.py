from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List

from api.services.jwt.models import JwtRoles
from api.services.jwt.service import AbstractJwtService
from shared.entities.email_verification.repo import AbstractEmailVerificationRepo
from shared.entities.refresh_token.repo import AbstractRefreshTokenRepo
from shared.entities.user.repo import AbstractUserRepo
from shared.settings import Settings
from shared.utils import validate_password
from .models import AccessTokenSet, RefreshTokenSet


class AbstractAuthService(ABC):
    class UserNotFound(Exception): ...

    class InvalidPassword(Exception): ...

    class UsernameExists(Exception): ...

    class EmailExists(Exception): ...

    class InvalidRefreshToken(Exception): ...

    class InvalidVerifyId(Exception): ...

    class InvalidCode(Exception): ...

    @abstractmethod
    async def login(self, email: str, password: str) -> RefreshTokenSet: ...

    @abstractmethod
    async def register(
        self, email: str, username: str, password: str
    ) -> AccessTokenSet | RefreshTokenSet: ...

    @abstractmethod
    async def refresh(self, refresh_token: str) -> RefreshTokenSet: ...

    @abstractmethod
    async def verify(
        self, user_id: int, email_verification_id: int, code: str
    ) -> RefreshTokenSet: ...


class DefaultAuthService(AbstractAuthService):
    def __init__(
        self,
        user_repo: AbstractUserRepo,
        refresh_token_repo: AbstractRefreshTokenRepo,
        email_verification_repo: AbstractEmailVerificationRepo,
        jwt_service: AbstractJwtService,
        settings: Settings,
    ):
        super().__init__()
        self.user_repo = user_repo
        self.refresh_token_repo = refresh_token_repo
        self.email_verification_repo = email_verification_repo
        self.jwt_service = jwt_service
        self.settings = settings

    def _generate_jwt_set_email(
        self, user_id: int, roles: List[str], email_verify: int
    ):
        jwt = self.jwt_service.new(user_id, roles, email_verify)
        return AccessTokenSet(
            access_token=jwt,
            access_token_expires_in=self.settings.access_token_expires_in,
        )

    def _generate_jwt_set(self, user_id: int, roles: List[str]) -> AccessTokenSet:
        jwt = self.jwt_service.new(user_id, roles)
        return AccessTokenSet(
            access_token=jwt,
            access_token_expires_in=self.settings.access_token_expires_in,
        )

    async def _generate_complete_jwt_set(
        self, user_id: int, roles: List[str]
    ) -> RefreshTokenSet:
        jwt = self.jwt_service.new(user_id, roles)
        refresh = await self.refresh_token_repo.commit_new(user_id)
        return RefreshTokenSet(
            access_token=jwt,
            refresh_token=str(refresh.id),
            access_token_expires_in=self.settings.access_token_expires_in,
            refresh_token_expires_in=self.settings.refresh_token_expires_in,
        )

    async def login(self, email: str, password: str) -> RefreshTokenSet:
        user = await self.user_repo.find_by_email(email)
        if user is None:
            raise AbstractAuthService.UserNotFound
        if not validate_password(user.password_hash, password):
            raise AbstractAuthService.InvalidPassword
        return await self._generate_complete_jwt_set(user.id, [JwtRoles.API])

    async def register(
        self, email: str, username: str, password: str
    ) -> AccessTokenSet | RefreshTokenSet:
        match await self.user_repo.lookup_by_email_or_username(email, username):
            case "email":
                raise AbstractAuthService.EmailExists
            case "username":
                raise AbstractAuthService.UsernameExists
        if self.settings.email_verification_enable:
            raise NotImplementedError
            # user = await self.user_repo.commit_new(email, username, password, False)
            # email_verify = await self.email_verification_repo.commit_new(user.id)
            # # send email
            # return self._generate_jwt_set_email(user.id, [JwtRoles.EMAIL_VERIFICATION], email_verify.id)
        else:
            user = await self.user_repo.commit_new(email, username, password, True)
            return await self._generate_complete_jwt_set(user.id, [JwtRoles.API])

    async def refresh(self, refresh_token: str) -> RefreshTokenSet:
        token = await self.refresh_token_repo.find_by_id(refresh_token)
        if token is None:
            raise AbstractAuthService.InvalidRefreshToken
        if (
            token.created_at + timedelta(seconds=self.settings.refresh_token_expires_in)
        ) < datetime.now():
            await self.refresh_token_repo.commit_del(token)
            raise AbstractAuthService.InvalidRefreshToken
        return await self._generate_complete_jwt_set(token.user_id, [JwtRoles.API])

    async def verify(
        self, user_id: int, email_verify_id: int, code: str
    ) -> RefreshTokenSet:
        verify = await self.email_verification_repo.find_by_id(email_verify_id)
        if verify is None:
            raise AbstractAuthService.InvalidVerifyId
        if verify.code != code:
            raise AbstractAuthService.InvalidCode
        await self.user_repo.enable(user_id)
        return await self._generate_complete_jwt_set(user_id, [JwtRoles.API])
