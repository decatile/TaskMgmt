from typing import Literal, cast
from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from shared.dal.models import User
from api.utils.hash import hash_password


class AbstractUserRepo(ABC):
    @abstractmethod
    async def find_by_id(self, id: int) -> User | None: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def lookup_by_email_or_username(
        self, email: str, username: str
    ) -> Literal["email", "username"] | None: ...

    @abstractmethod
    async def commit_new(self, email: str, username: str, password: str) -> User: ...


class DatabaseUserRepo(AbstractUserRepo):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def find_by_id(self, id: int) -> User | None:
        return cast(
            User | None, await self.session.scalar(select(User).where(User.id == id))
        )

    async def find_by_email(self, email: str) -> User | None:
        return cast(
            User | None,
            await self.session.scalar(select(User).where(User.email == email)),
        )

    async def lookup_by_email_or_username(
        self, email: str, username: str
    ) -> Literal["email", "username"] | None:
        user = cast(
            User | None,
            await self.session.scalar(
                select(User).where((User.email == email) | (User.username == username))
            ),
        )
        if user is None:
            return None
        return None if user is None else "email" if user.email == email else "username"

    async def commit_new(self, email: str, username: str, password: str) -> User:
        user = User(
            email=email, username=username, password_hash=hash_password(password)
        )
        self.session.add(user)
        await self.session.flush()
        return user
