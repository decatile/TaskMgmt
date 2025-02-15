from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import delete, func
from shared.entities.refresh_token import RefreshToken
from shared.entities.email_verification import EmailVerification
from shared.settings import Settings
from logging import getLogger
import asyncio

log = getLogger(__name__)

settings = Settings()  # type: ignore
engine = create_async_engine(settings.database_url)
app = Celery("cleanup_refresh_tokens", broker=settings.redis_url)
app.conf.beat_schedule = {
    "cleanup-refresh-tokens": {
        "task": "worker.cleanup_refresh_tokens.task",
        "schedule": crontab(hour="*/1"),
    }
}


@app.task
def task():
    asyncio.get_event_loop().run_until_complete(__task())


async def __task():
    async with engine.begin() as c:
        tokens = await c.execute(
            delete(RefreshToken).where(
                (
                    RefreshToken.created_at
                    + timedelta(seconds=settings.refresh_token_expires_in)
                )
                < func.now()
            )
        )
        emails = await c.execute(
            delete(EmailVerification).where(
                (
                    EmailVerification.created_at
                    + timedelta(seconds=settings.email_verification_code_expires_in)
                )
                < func.now()
            )
        )
        log.info(
            "Performed cleanup | Refresh token (%d) and Email verification (%d)",
            tokens.rowcount,
            emails.rowcount,
        )
