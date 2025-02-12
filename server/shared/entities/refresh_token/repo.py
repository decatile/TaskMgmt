from abc import abstractmethod
from sqlalchemy import func
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from shared.abc.expirable_repository import ABCExpirableRepository, ExpirableRepository
from shared.settings import Settings
from shared.entities.refresh_token import RefreshToken


class ABCRefreshTokenRepository(ABCExpirableRepository[RefreshToken, str]):
    @abstractmethod
    def new(self, user_id: int) -> RefreshToken: ...


class DatabaseRefreshTokenRepository(
    ExpirableRepository[RefreshToken, str], ABCRefreshTokenRepository
):
    def __init__(self, session: AsyncSession, settings: Settings):
        super().__init__(
            RefreshToken,
            session,
            lambda _: (
                RefreshToken.created_at
                + timedelta(seconds=self.__settings.refresh_token_expires_in)
            )
            < func.now(),
        )
        self.__settings = settings

    def new(self, user_id: int) -> RefreshToken:
        return RefreshToken(user_id=user_id)
