from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from shared.entities.email_verification import (
    EmailVerificationRepository,
)
from api.di.session import get_session


def get_email_verification_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> EmailVerificationRepository:
    return EmailVerificationRepository(session)
