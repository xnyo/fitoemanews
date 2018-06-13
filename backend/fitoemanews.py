import asyncio
import sys

from singletons.config import Config
from singletons.emanews import EmaNews


def main():
    c = Config()
    EmaNews(
        db_host=c["DB_HOST"],
        db_port=c["DB_PORT"],
        db_username=c["DB_USERNAME"],
        db_password=c["DB_PASSWORD"],
        db_database=c["DB_NAME"],
        db_pool_minsize=c["DB_POOL_MIN_SIZE"],
        db_pool_maxsize=c["DB_POOL_MAX_SIZE"],
        debug=c["DEBUG"],
        web_host=c["HTTP_HOST"],
        web_port=c["HTTP_PORT"],
        redis_host=c["REDIS_HOST"],
        redis_port=c["REDIS_PORT"],
        redis_password=c["REDIS_PASSWORD"],
        redis_database=c["REDIS_DATABASE"],
        redis_pool_size=c["REDIS_POOL_SIZE"],
        telegram_token=c["TELEGRAM_TOKEN"]
    )
    if len(sys.argv) >= 2 and sys.argv[1] == "scrape":
        EmaNews().initialize()
        loop = asyncio.get_event_loop()
        from jobs import scraper
        loop.run_until_complete(scraper.scrape_everything())
    else:
        EmaNews().start()


if __name__ == '__main__':
    main()
