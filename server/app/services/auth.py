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

    @abstractmethod
    async def login(self, username: str, password: str) -> TokenSet: ...


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

    async def login(self, username: str, password: str) -> TokenSet:
        user = await self.user_repo.find_by_username(username)
        if user is None:
            raise AbstractAuthService.UserNotFound
        if not validate_password(user.password_hash, password):
            raise AbstractAuthService.InvalidPassword
        jwt = self.jwt_service.new(user.id)
        refresh = await self.refresh_token_repo.commit_new(user.id)
        return TokenSet(
            access_token=jwt.string,
            refresh_token=refresh.id,
            access_token_expires_in=jwt.expires_in,
            refresh_token_expires_in=refresh.expires_in,
        )
