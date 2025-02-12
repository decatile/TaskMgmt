# type: ignore
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
from sqlalchemy import delete, func
from sqlalchemy.ext.asyncio import create_async_engine
from shared.dal.models.refresh_token import RefreshToken
from api.di.database_config import get_database_config
from api.di.redis_config import get_redis_config
from api.di.token_config import get_token_config


redis = get_redis_config()
token = get_token_config()
database = get_database_config()
engine = create_async_engine(database.url)

app = Celery("worker", broker=redis.url)
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
                    + timedelta(seconds=token.refresh_token_expires_in)
                )
                < func.now()
            )
        )
