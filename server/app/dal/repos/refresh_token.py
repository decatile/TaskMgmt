from abc import ABC, abstractmethod
from typing import cast
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.token import TokenConfig
from app.dal.models import RefreshToken


class AbstractRefreshTokenRepo(ABC):
    @abstractmethod
    async def find_by_id(self, id: str) -> RefreshToken | None: ...

    @abstractmethod
    async def commit_new(self, user_id: int) -> RefreshToken: ...


class DatabaseRefreshTokenRepo(AbstractRefreshTokenRepo):
    def __init__(self, session: AsyncSession, config: TokenConfig):
        super().__init__()
        self.session = session
        self.config = config

    async def find_by_id(self, id: str) -> RefreshToken | None:
        return cast(
            RefreshToken | None,
            await self.session.scalar(select(RefreshToken.id == id)),
        )

    async def commit_new(self, user_id: int) -> RefreshToken:
        token = RefreshToken(
            expires_in=self.config.refresh_token_expires_in, user_id=user_id
        )
        self.session.add(token)
        await self.session.commit()
        return token
