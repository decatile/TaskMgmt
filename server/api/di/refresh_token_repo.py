from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from shared.entities.refresh_token import (
    RefreshTokenRepository,
)
from api.di.session import get_session


def get_refresh_token_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> RefreshTokenRepository:
    return RefreshTokenRepository(session)
