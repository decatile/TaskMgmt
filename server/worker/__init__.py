# type: ignore
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
from sqlalchemy import delete, func
from sqlalchemy.ext.asyncio import create_async_engine
from shared.dal.models.refresh_token import RefreshToken
from shared.settings import settings

engine = create_async_engine(settings.database_url)
app = Celery("worker", broker=settings.redis_url)
app.conf.beat_schedule = {
    "cleanup-refresh-tokens": {
        "task": "worker.cleanup_refresh_tokens",
        "schedule": crontab(minute=0, hour="*/1"),
    }
}


@app.task
async def cleanup_refresh_tokens():
    async with engine.begin() as c:
        await c.execute(
            delete(RefreshToken).where(
                (
                    RefreshToken.created_at
                    + timedelta(seconds=settings.refresh_token_expires_in)
                )
                < func.now()
            )
        )
