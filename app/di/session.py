from os import environ
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine(environ["DATABASE_URL"])


def get_session() -> AsyncSession:
    return AsyncSession(engine)
