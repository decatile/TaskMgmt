from typing import Literal, cast
from abc import ABC, abstractmethod
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from shared.entities.user import User
from shared.utils import hash_password


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
    async def commit_new(
        self, email: str, username: str, password: str, enabled: bool
    ) -> User: ...

    @abstractmethod
    async def enable(self, user_id: int) -> None: ...


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

    async def commit_new(
        self, email: str, username: str, password: str, enabled: bool
    ) -> User:
        user = User(
            email=email,
            username=username,
            password_hash=hash_password(password),
            enabled=enabled,
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def enable(self, user_id: int) -> None:
        await self.session.execute(
            update(User).where(User.id == user_id).values(enabled=True)
        )
