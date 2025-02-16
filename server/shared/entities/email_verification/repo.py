from sqlalchemy.ext.asyncio import AsyncSession
from shared.abc import Repository
from shared.entities.email_verification import EmailVerification
from random import randint


class EmailVerificationRepository(Repository[EmailVerification, str]):
    def __init__(self, session: AsyncSession):
        super().__init__(
            EmailVerification,
            session,
        )

    def new(self, user_id: int) -> EmailVerification:
        return EmailVerification(
            code=str(randint(0, 9999)).zfill(4),
            user_id=user_id,
        )
