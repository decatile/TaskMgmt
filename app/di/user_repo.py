from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dal.repos.user import AbstractUserRepo, DatabaseUserRepo
from app.di.session import get_session


def get_user_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AbstractUserRepo:
    return DatabaseUserRepo(session)
