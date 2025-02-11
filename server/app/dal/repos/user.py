from typing import Literal, cast
from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.dal.models import User
from app.utils.hash import hash_password


class AbstractUserRepo(ABC):
    @abstractmethod
    async def find_by_username(self, username: str) -> User | None: ...

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

    async def find_by_username(self, username: str) -> User | None:
        return cast(
            User | None,
            await self.session.scalar(select(User).where(User.username == username)),
        )

    async def lookup_by_email_or_username(
        self, email: str, username: str
    ) -> Literal["email", "username"] | None:
        user = cast(
            User | None,
            await self.session.scalar(
                select(User).where(User.email == email or User.username == username)
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
        await self.session.commit()
        return user
