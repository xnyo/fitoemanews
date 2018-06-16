import asyncio
import logging
import sys

from singletons.config import Config
from singletons.emanews import EmaNews
from utils.mailgun import MailgunClient, DummyMailgunClient


def main(test_mode=False):  # pragma: nocover
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    test_mode = "testmode" in sys.argv or test_mode
    if test_mode:
        logging.getLogger().warning("Starting EmaNews with test configuration!")
    c = Config()
    EmaNews(
        db_host=c["DB_HOST"],
        db_port=c["DB_PORT"],
        db_username=c["DB_USERNAME"],
        db_password=c["DB_PASSWORD"],
        db_database=c["DB_NAME"] if not test_mode else c["TEST_DB_NAME"],
        db_pool_minsize=c["DB_POOL_MIN_SIZE"],
        db_pool_maxsize=c["DB_POOL_MAX_SIZE"],
        debug=c["DEBUG"],
        web_host=c["HTTP_HOST"],
        web_port=c["HTTP_PORT"],
        redis_host=c["REDIS_HOST"],
        redis_port=c["REDIS_PORT"],
        redis_password=c["REDIS_PASSWORD"],
        redis_database=c["REDIS_DATABASE"] if not test_mode else c["REDIS_TEST_DATABASE"],
        redis_pool_size=c["REDIS_POOL_SIZE"],
        telegram_token=c["TELEGRAM_TOKEN"],
        mailgun_client=MailgunClient(
            domain=c["MAILGUN_DOMAIN"],
            key=c["MAILGUN_KEY"],
            default_from=c["MAILGUN_DEFAULT_SENDER"]
        ) if c["MAILGUN_KEY"] is not None else DummyMailgunClient()
    )
    if "scrape" in sys.argv:
        EmaNews().initialize()
        loop = asyncio.get_event_loop()
        from jobs import scraper
        loop.run_until_complete(scraper.scrape_everything())
    else:
        EmaNews().start()


if __name__ == '__main__':  # pragma: nocover
    main()
