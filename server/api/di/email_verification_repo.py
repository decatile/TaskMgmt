from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.di.settings import get_settings
from shared.entities.email_verification import (
    AbstractEmailVerificationRepo,
    DatabaseEmailVerificationRepo,
)
from shared.settings import Settings
from api.di.session import get_session


def get_email_verification_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AbstractEmailVerificationRepo:
    return DatabaseEmailVerificationRepo(session, settings)
