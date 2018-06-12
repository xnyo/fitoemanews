import asyncio
import logging
from typing import Optional

import aiomysql
import aioredis
from aiohttp import web
from aiomysql import DictCursor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from migrator.migrator import Migrator
from utils.singletons import singleton


@singleton
class EmaNews:
    """
    Singleton EmaNews
    """
    logger = logging.getLogger("emanews")

    def __init__(
        self,
        db_host: str = None, db_username: str = None,
        db_password: str = None, db_database: str = None,
        db_port: int = 3306, db_pool_minsize: int=None,
        redis_host: str = "127.0.0.1", redis_port: int = 6379,
        redis_database: int = 0, redis_password: str = None,
        redis_pool_size: int = 8, db_pool_maxsize: int=None,
        web_host: Optional[str]=None, web_port: Optional[int]=None,
        debug: bool = False
    ):
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

        logging.basicConfig(level=logging.DEBUG if self.debug else logging.INFO)

        self._initialized = False
        self.app: web.Application = None
        self.db: aiomysql.Pool = None
        self.redis: aioredis.Redis = None
        self.scheduler: AsyncIOScheduler = None

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
        from api.handlers import ping, zxcvbn_strength, user, activate, login, logout, herbs
        self.app: web.Application() = web.Application()
        self.app.add_routes([
            web.get("/api/v1/ping", ping.handle),
            web.get("/api/v1/zxcvbn", zxcvbn_strength.handle),
            web.post("/api/v1/user", user.post),
            web.get("/api/v1/user", user.get),
            web.post("/api/v1/activate/{token}", activate.handle),
            web.post("/api/v1/login", login.handle),
            web.post("/api/v1/logout", logout.handle),
            web.get("/api/v1/herbs", herbs.handle)
        ])

    def initialize_scheduler(self):
        """
        Crea lo schedulatore e registra i jobs

        :return:
        """
        self.scheduler = AsyncIOScheduler()
        from jobs import scraper

    def initialize(self):
        """
        Inizializza EmaNews

        :return:
        """
        loop = asyncio.get_event_loop()

        self.logger.info("Initializing fitoemanews")

        # Registra route aiohttp
        self.initialize_web_app()

        # Connetti al db
        loop.run_until_complete(self.connect_db())

        # Connetti a redis
        loop.run_until_complete(self.connect_redis())

        # Esegui migrations
        loop.run_until_complete(Migrator(self.db).migrate())

        # Registra job nello schedulatore
        self.initialize_scheduler()

        self._initialized = True

    def start(self):
        """
        Inizializza (se necessario) e avvia EmaNews

        :return:
        """
        if not self._initialized:
            self.initialize()
        self.scheduler.start()
        self.app.on_cleanup.append(self.dispose)
        self.logger.info("Web API listening on {}:{}".format(self.web_host, self.web_port))
        logging.getLogger("aiohttp.access").setLevel(logging.DEBUG if self.debug else logging.CRITICAL)
        try:
            web.run_app(self.app, port=self.web_port, print=None)
        finally:
            self.logger.info("Goodbye!")
