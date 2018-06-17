import asyncio
import logging
from typing import Optional

import aiomysql
import aioredis
from aiohttp import web
from aiomysql import DictCursor
from aiotg import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from migrator.migrator import Migrator
from utils.mailgun import MailgunClient
from utils.singletons import singleton


@singleton
class EmaNews:
    """
    Singleton EmaNews
    """
    logger = logging.getLogger("emanews")

    def __init__(
        self, *,
        db_host: str = None, db_username: str = None,
        db_password: str = None, db_database: str = None,
        db_port: int = 3306, db_pool_minsize: int=None,
        redis_host: str = "127.0.0.1", redis_port: int = 6379,
        redis_database: int = 0, redis_password: str = None,
        redis_pool_size: int = 8, db_pool_maxsize: int=None,
        web_host: Optional[str]=None, web_port: Optional[int]=None,
        mailgun_client: MailgunClient=None,
        telegram_token: str=None,
        debug: bool = False, loop=None
    ):
        """
        Inizializza singleton EmaNews

        :param db_host: host database
        :param db_username: username database
        :param db_password: password database
        :param db_database: nome database
        :param db_port: port database
        :param db_pool_minsize: grandezza minima pool aiomysql
        :param db_pool_maxsize: grandezza massima pool aiomysql
        :param redis_host: host redis
        :param redis_port: porta redis
        :param redis_database: numero db redis
        :param redis_password: password redis
        :param redis_pool_size: grandezza pool redis
        :param web_host: ip su cui avviare il socket HTTP dell'API
        :param web_port: porta su cui avviare il socket HTTP dell'API
        :param mailgun_client: client mailgun
        :param telegram_token: token bot telegram
        :param debug: debug mode
        :param loop: IOLoop su cui avviare il server
        """
        self.db_host: str = db_host
        self.db_port: int = db_port
        self.db_username: str = db_username
        self.db_password: str = db_password
        self.db_database: str = db_database
        self.db_pool_minsize: int = db_pool_minsize
        self.db_pool_maxsize: int = db_pool_maxsize
        self.redis_host: str = redis_host
        self.redis_port: int = redis_port
        self.redis_database: int = redis_database
        self.redis_password: str = redis_password
        self.redis_pool_size: int = redis_pool_size
        self.debug: bool = debug
        self.web_host: str = web_host
        self.web_port: int = web_port
        self.telegram_token: str = telegram_token
        self.mailgun_client: MailgunClient = mailgun_client

        logging.basicConfig(level=logging.DEBUG if self.debug else logging.INFO)

        self._initialized = False
        self.app: web.Application = None
        self.db: aiomysql.Pool = None
        self.redis: aioredis.Redis = None
        self.scheduler: AsyncIOScheduler = None
        self.bot: Bot = None
        self.loop = loop if loop is not None else asyncio.get_event_loop()

    async def connect_db(self):
        """
        Crea un pool di connessioni al database

        :return:
        """
        self.logger.info("Connecting to db...")
        self.db = await aiomysql.create_pool(
            host=self.db_host, port=self.db_port,
            user=self.db_username, password=self.db_password,
            db=self.db_database, minsize=self.db_pool_minsize,
            maxsize=self.db_pool_maxsize, cursorclass=DictCursor,
            charset="utf8", use_unicode=True
        )

    async def connect_redis(self):
        """
        Crea un pool di connessioni a redis

        :return:
        """
        self.logger.info("Connecting to redis...")
        self.redis = await aioredis.create_redis_pool(
            address=(self.redis_host, self.redis_port),
            db=self.redis_database,
            password=self.redis_password,
            maxsize=self.redis_pool_size
        )

    async def dispose(self, _=None):
        """
        Chiude le risorse aperte dal web server.
        Da chiamare prima della chiusura.

        :return:
        """
        self.logger.info("Disposing emanews")

        self.logger.info("Closing db pool...")
        self.db.terminate()
        await self.db.wait_closed()

        self.logger.info("Closing redis pool...")
        self.redis.close()
        await self.redis.wait_closed()

        self.logger.info("Stopping scheduler...")
        self.scheduler.shutdown()

    def initialize_web_app(self):
        """
        Crea l'app aiohttp e registra le routes

        :return:
        """
        from api.handlers import ping, zxcvbn_strength, user, activate, login, logout, herbs, notification_settings, \
            telegram, api_key
        self.app: web.Application() = web.Application()
        self.app.add_routes([
            web.get("/api/v1/ping", ping.handle),
            web.get("/api/v1/zxcvbn", zxcvbn_strength.handle),
            web.post("/api/v1/user", user.post),
            web.get("/api/v1/user", user.get),
            web.post("/api/v1/activate/{token}", activate.handle),
            web.post("/api/v1/login", login.handle),
            web.post("/api/v1/logout", logout.handle),
            web.get("/api/v1/herbs", herbs.handle),
            web.get("/api/v1/notification_settings", notification_settings.get),
            web.post("/api/v1/notification_settings", notification_settings.post),
            web.get("/api/v1/telegram", telegram.get),
            web.delete("/api/v1/telegram", telegram.delete),
            web.get("/api/v1/api_keys", api_key.get),
            web.post("/api/v1/api_keys", api_key.post),
            web.delete("/api/v1/api_keys/{id_}", api_key.delete),
        ])

    def initialize_scheduler(self):
        """
        Crea lo schedulatore e registra i jobs

        :return:
        """
        self.scheduler = AsyncIOScheduler(event_loop=self.loop)
        from jobs import scraper

    def initialize_bot(self):
        """
        Inizializza il bot di telegram

        :return:
        """
        self.bot = Bot(api_token=self.telegram_token)
        from bot import start

    def initialize(self):
        """
        Inizializza EmaNews

        :return:
        """
        if self._initialized:   # pragma: nocover
            raise RuntimeError("EmaNews already initialized")
        loop = asyncio.get_event_loop()

        self.logger.info("Initializing fitoemanews")

        # Registra route aiohttp
        self.initialize_web_app()

        # Crea bot
        self.initialize_bot()

        # Connetti al db
        loop.run_until_complete(self.connect_db())

        # Connetti a redis
        loop.run_until_complete(self.connect_redis())

        # Esegui migrations
        loop.run_until_complete(Migrator(self.db).migrate())

        # Registra job nello schedulatore
        self.initialize_scheduler()

        self._initialized = True

    def start(self):    # pragma: nocover
        """
        Inizializza (se necessario) e avvia EmaNews

        :return:
        """
        if not self._initialized:
            self.initialize()
        self.scheduler.start()
        self.app.on_cleanup.append(self.dispose)

        # Crea runner aiohttp, per avviare insieme sia aiohttp che aiotg
        runner = web.AppRunner(self.app)
        self.loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, port=self.web_port)
        logging.getLogger("aiohttp.access").setLevel(logging.DEBUG if self.debug else logging.CRITICAL)

        try:
            # aiohttp
            self.logger.info("Web API listening on {}:{}".format(self.web_host, self.web_port))
            asyncio.ensure_future(site.start())

            # aiotg, se necessario
            if self.is_bot_enabled:
                self.logger.info("Starting Telegram bot")
                bot_loop = asyncio.ensure_future(self.bot.loop())
            else:
                self.logger.warning("Telegram bot is disabled")

            # Avvia IOLoop
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user")
        finally:
            # Chiudi loop web e aiotg
            if self.is_bot_enabled:
                bot_loop.cancel()
                self.bot.stop()
                self.loop.run_until_complete(self.bot.session.close())
            self.loop.run_until_complete(runner.cleanup())
            self.loop.stop()
            self.loop.close()
            self.logger.info("Goodbye!")

    @property
    def is_bot_enabled(self) -> bool:   # pragma: nocover
        return self.telegram_token is not None
