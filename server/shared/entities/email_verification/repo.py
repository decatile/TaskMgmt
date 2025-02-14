from sqlalchemy.ext.asyncio import AsyncSession
from shared.abc import Repository
from shared.entities.email_verification import EmailVerification
from shared.settings import Settings
from random import randint


class EmailVerificationRepository(Repository[EmailVerification, int]):
    def __init__(self, session: AsyncSession, settings: Settings):
        super().__init__(
            EmailVerification,
            session,
        )
        self._settings = settings

    def new(self, user_id: int) -> EmailVerification:
        return EmailVerification(
            code=str(randint(0, 9999)).zfill(4),
            user_id=user_id,
        )
