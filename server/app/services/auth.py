from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.dal.repos.refresh_token import AbstractRefreshTokenRepo
from app.dal.repos.user import AbstractUserRepo
from app.services.jwt import AbstractJwtService
from app.utils.hash import validate_password


class TokenSet(BaseModel):
    access_token: str
    refresh_token: str
    access_token_expires_in: int
    refresh_token_expires_in: int


class AbstractAuthService(ABC):
    class UserNotFound(Exception): ...

    class InvalidPassword(Exception): ...

    class UsernameExists(Exception): ...

    class EmailExists(Exception): ...

    @abstractmethod
    async def login(self, username: str, password: str) -> TokenSet: ...

    @abstractmethod
    async def register(cls, email: str, username: str, password: str) -> TokenSet: ...


class DefaultAuthService(AbstractAuthService):
    def __init__(
        self,
        user_repo: AbstractUserRepo,
        refresh_token_repo: AbstractRefreshTokenRepo,
        jwt_service: AbstractJwtService,
    ):
        super().__init__()
        self.user_repo = user_repo
        self.refresh_token_repo = refresh_token_repo
        self.jwt_service = jwt_service

    async def _generate_jwt_set(self, user_id: int) -> TokenSet:
        jwt = self.jwt_service.new(user_id)
        refresh = await self.refresh_token_repo.commit_new(user_id)
        return TokenSet(
            access_token=jwt.string,
            refresh_token=refresh.id,
            access_token_expires_in=jwt.expires_in,
            refresh_token_expires_in=refresh.expires_in,
        )

    async def login(self, username: str, password: str) -> TokenSet:
        user = await self.user_repo.find_by_username(username)
        if user is None:
            raise AbstractAuthService.UserNotFound
        if not validate_password(user.password_hash, password):
            raise AbstractAuthService.InvalidPassword
        return await self._generate_jwt_set(user.id)

    async def register(self, email: str, username: str, password: str) -> TokenSet:
        match await self.user_repo.lookup_by_email_or_username(email, username):
            case "email":
                raise AbstractAuthService.EmailExists
            case "username":
                raise AbstractAuthService.UsernameExists
        user = await self.user_repo.commit_new(email, username, password)
        return await self._generate_jwt_set(user.id)
