from abc import ABC, abstractmethod
from typing import cast
from sqlalchemy import select, delete, func
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from shared.dal.models.email_verification import EmailVerification
from shared.settings import Settings
from random import randint


class AbstractEmailVerificationRepo(ABC):
    @abstractmethod
    async def find_by_id(self, id: int) -> EmailVerification | None: ...

    @abstractmethod
    async def commit_new(self, user_id: int) -> EmailVerification: ...

    @abstractmethod
    async def commit_del(self, token: EmailVerification) -> None: ...

    @abstractmethod
    async def remove_expired(self) -> int: ...


class DatabaseEmailVerificationRepo(AbstractEmailVerificationRepo):
    def __init__(self, session: AsyncSession, settings: Settings):
        super().__init__()
        self.session = session
        self.settings = settings

    async def find_by_id(self, id: int) -> EmailVerification | None:
        return cast(
            EmailVerification | None,
            await self.session.scalar(select(EmailVerification.id == id)),
        )

    async def commit_new(self, user_id: int) -> EmailVerification:
        token = EmailVerification(
            code=str(randint(0, 9999)).zfill(4),
            expires_in=self.settings.refresh_token_expires_in, user_id=user_id
        )
        self.session.add(token)
        await self.session.flush()
        return token

    async def commit_del(self, token: EmailVerification) -> None:
        await self.session.delete(token)

    async def remove_expired(self) -> int:
        result = await self.session.execute(
            delete(EmailVerification).where(
                (
                    EmailVerification.created_at
                    + timedelta(
                        seconds=self.settings.email_verification_code_expires_in
                    )
                )
                < func.now()
            )
        )
        return result.rowcount
