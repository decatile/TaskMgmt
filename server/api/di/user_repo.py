from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from shared.entities.user import AbstractUserRepo, DatabaseUserRepo
from api.di.session import get_session


def get_user_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AbstractUserRepo:
    return DatabaseUserRepo(session)
