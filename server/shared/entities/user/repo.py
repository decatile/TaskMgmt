from typing import Literal
from abc import abstractmethod
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from shared.utils import hash_password
from shared.abc.repository import ABCRepository, Repository
from shared.entities.user import User


class ABCUserRepository(ABCRepository[User, int]):
    @abstractmethod
    async def find_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def lookup_by_email_or_username(
        self, email: str, username: str
    ) -> Literal["none", "email", "username"]: ...

    @abstractmethod
    def new(self, email: str, username: str, password: str, enabled: bool) -> User: ...

    @abstractmethod
    async def enable(self, user_id: int) -> None: ...


class DatabaseUserRepository(Repository[User, int], ABCUserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def find_by_email(self, email: str) -> User | None:
        return await self._session.scalar(select(User).where(User.email == email))

    async def lookup_by_email_or_username(
        self, email: str, username: str
    ) -> Literal["none", "email", "username"]:
        user = await self._session.scalar(
            select(User).where((User.email == email) | (User.username == username))
        )
        if user is None:
            return "none"
        if user.email == email:
            return "email"
        return "username"

    def new(self, email: str, username: str, password: str, enabled: bool):
        return User(
            email=email,
            username=username,
            password_hash=hash_password(password),
            enabled=enabled,
        )

    async def enable(self, user_id) -> None:
        await self._session.execute(
            update(User).where(User.id == user_id).values(enabled=True)
        )
