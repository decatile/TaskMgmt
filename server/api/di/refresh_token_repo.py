from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from shared.config.token import TokenConfig
from shared.dal.repos.refresh_token import (
    AbstractRefreshTokenRepo,
    DatabaseRefreshTokenRepo,
)
from api.di.session import get_session
from api.di.token_config import get_token_config


def get_refresh_token_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
    token_config: Annotated[TokenConfig, Depends(get_token_config)],
) -> AbstractRefreshTokenRepo:
    return DatabaseRefreshTokenRepo(session, token_config)
