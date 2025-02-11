from typing import cast
from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.dal.models import User


class AbstractUserRepo(ABC):
    @abstractmethod
    async def find_by_username(self, username: str) -> User | None: ...


class DatabaseUserRepo(AbstractUserRepo):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def find_by_username(self, username: str) -> User | None:
        return cast(
            User | None,
            await self.session.scalar(select(User).where(User.username == username)),
        )
