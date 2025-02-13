from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from api.di.settings import get_settings
from shared.settings import Settings

engine: AsyncEngine | None = None


async def get_session(
    settings: Annotated[Settings, Depends(get_settings)],
) -> AsyncGenerator[AsyncSession]:
    global engine
    if engine is None:
        engine = create_async_engine(settings.database_url)
    async with AsyncSession(engine) as session, session.begin() as tx:
        yield tx.session
