# type: ignore
from celery import Celery
from celery.schedules import crontab
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from shared.entities.refresh_token import RefreshTokenRepository
from shared.entities.email_verification import EmailVerificationRepository
from shared.settings import settings

engine = create_async_engine(settings.database_url)
app = Celery("cleanup_refresh_tokens", broker=settings.redis_url)
app.conf.beat_schedule = {
    "cleanup-refresh-tokens": {
        "task": "cleanup_refresh_tokens.task",
        "schedule": crontab(minute=0, hour="*/1"),
    }
}


@app.task
async def task():
    async with AsyncSession(engine) as session, engine.begin():
        await RefreshTokenRepository(session, settings).cleanup_expired()
        await EmailVerificationRepository(session, settings).cleanup_expired()
