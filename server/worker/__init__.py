# type: ignore
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
from sqlalchemy import create_engine, delete, func
from shared.dal.models.refresh_token import RefreshToken
from api.di.database_config import get_database_config
from api.di.redis_config import get_redis_config
from api.di.token_config import get_token_config


redis = get_redis_config()
token = get_token_config()
database = get_database_config()
engine = create_engine(database.url)

app = Celery("worker", broker=redis.url)
app.conf.beat_schedule = {
    "cleanup-refresh-tokens": {
        "task": "worker.cleanup_refresh_tokens",
        "schedule": crontab(minute=0, hour="*/1"),
    }
}


@app.task
def cleanup_refresh_tokens():
    with engine.begin() as c:
        c.execute(
            delete(RefreshToken).where(
                (
                    RefreshToken.created_at
                    + timedelta(seconds=token.refresh_token_expires_in)
                )
                < func.now()
            )
        )
