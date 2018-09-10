import logging

from apscheduler.triggers.interval import IntervalTrigger

from singletons.emanews import EmaNews
from utils import raven

emanews = EmaNews()
logger = logging.getLogger("cleanup")


@emanews.scheduler.scheduled_job(
    IntervalTrigger(minutes=2)
)
@raven.capture
async def clean_expired_password_reset_tokens():
    logging.info("Cleaning expired password reset tokens")
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM password_reset_tokens WHERE `expire` <= UNIX_TIMESTAMP()")
            await conn.commit()


@emanews.scheduler.scheduled_job(
    IntervalTrigger(minutes=2)
)
@raven.capture
async def clean_expired_telegram_link_tokens():
    logging.info("Cleaning expired telegram link tokens")
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM telegram_link_tokens WHERE `expire` <= UNIX_TIMESTAMP()")
            await conn.commit()
