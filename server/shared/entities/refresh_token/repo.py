from abc import ABC, abstractmethod
from typing import cast
from sqlalchemy import select, delete, func
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from shared.settings import Settings
from shared.entities.refresh_token import RefreshToken


class AbstractRefreshTokenRepo(ABC):
    @abstractmethod
    async def find_by_id(self, id: str) -> RefreshToken | None: ...

    @abstractmethod
    async def create_new_token(self, user_id: int) -> RefreshToken: ...

    @abstractmethod
    async def delete_by_id(self, token_id: str) -> None: ...

    @abstractmethod
    async def delete_token(self, token: RefreshToken) -> None: ...

    @abstractmethod
    async def delete_expired_tokens(self) -> int: ...


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

    async def create_new_token(self, user_id: int) -> RefreshToken:
        token = RefreshToken(user_id=user_id)
        self.session.add(token)
        await self.session.flush()
        return token

    async def delete_by_id(self, token_id: str) -> None:
        await self.session.execute(
            delete(RefreshToken).where(RefreshToken.id == token_id)
        )

    async def delete_token(self, token: RefreshToken) -> None:
        await self.session.delete(token)

    async def delete_expired_tokens(self) -> int:
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
