from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from app.config.database import DatabaseConfig
from app.di.database_config import get_database_config

engine: AsyncEngine | None = None


async def get_session(
    config: Annotated[DatabaseConfig, Depends(get_database_config)],
) -> AsyncGenerator[AsyncSession]:
    global engine
    if engine is None:
        engine = create_async_engine(config.url)
    async with AsyncSession(engine) as session, session.begin():
        yield session
