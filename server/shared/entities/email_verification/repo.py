from sqlalchemy import func
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from shared.abc import ExpirableRepository
from shared.entities.email_verification import EmailVerification
from shared.settings import Settings
from random import randint


class EmailVerificationRepository(ExpirableRepository[EmailVerification, int]):
    def __init__(self, session: AsyncSession, settings: Settings):
        super().__init__(
            EmailVerification,
            session,
            lambda _: (
                EmailVerification.created_at
                + timedelta(seconds=self._settings.email_verification_code_expires_in)
            )
            < func.now(),
        )
        self._settings = settings

    def new(self, user_id: int) -> EmailVerification:
        return EmailVerification(
            code=str(randint(0, 9999)).zfill(4),
            expires_in=self._settings.refresh_token_expires_in,
            user_id=user_id,
        )
