from abc import ABC, abstractmethod
from typing import cast
from sqlalchemy import select, delete, func
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from shared.settings import Settings
from shared.dal.models import RefreshToken


class AbstractRefreshTokenRepo(ABC):
    @abstractmethod
    async def find_by_id(self, id: str) -> RefreshToken | None: ...

    @abstractmethod
    async def commit_new(self, user_id: int) -> RefreshToken: ...

    @abstractmethod
    async def commit_del(self, token: RefreshToken) -> None: ...

    @abstractmethod
    async def remove_expired(self) -> int: ...


class DatabaseRefreshTokenRepo(AbstractRefreshTokenRepo):
    def __init__(self, session: AsyncSession, settings: Settings):
        super().__init__()
        self.session = session
        self.settings = settings

    async def find_by_id(self, id: str) -> RefreshToken | None:
        return cast(
            RefreshToken | None,
            await self.session.scalar(select(RefreshToken.id == id)),
        )

    async def commit_new(self, user_id: int) -> RefreshToken:
        token = RefreshToken(
            expires_in=self.settings.refresh_token_expires_in, user_id=user_id
        )
        self.session.add(token)
        await self.session.flush()
        return token

    async def commit_del(self, token: RefreshToken) -> None:
        await self.session.delete(token)
    
    async def remove_expired(self) -> int:
        result = await self.session.execute(
            delete(RefreshToken).where(
                (
                    RefreshToken.created_at
                    + timedelta(seconds=self.settings.refresh_token_expires_in)
                )
                < func.now()
            )
        )
        return result.rowcount
