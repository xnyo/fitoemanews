import asyncio
import logging

import aiomysql
from aiohttp import web
from aiohttp.web_routedef import RouteTableDef
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
        db_pool_maxsize: int=None, debug: bool=False,
        web_host: str=None, web_port: int=None
    ):
        self.db_host: str = db_host
        self.db_port: int = db_port
        self.db_username: str = db_username
        self.db_password: str = db_password
        self.db_database: str = db_database
        self.db_pool_minsize: int = db_pool_minsize
        self.db_pool_maxsize: int = db_pool_maxsize
        self.debug: bool = debug
        self.web_host: str = web_host
        self.web_port: int = web_port

        logging.basicConfig(level=logging.DEBUG if self.debug else logging.INFO)

        self._initialized = False
        self.app: web.Application = None
        self.routes: RouteTableDef = None
        self.db: aiomysql.Pool = None
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

    async def dispose(self, _):
        """
        Chiude le risorse aperte dal web server.
        Da chiamare prima della chiusura.

        :return:
        """
        self.logger.info("Disposing emanews")

        self.logger.info("Closing db pool...")
        self.db.terminate()
        await self.db.wait_closed()

        self.logger.info("Stopping scheduler...")
        self.scheduler.shutdown()

    def initialize_web_app(self):
        """
        Crea l'app aiohttp e registra le routes

        :return:
        """
        self.routes: RouteTableDef = RouteTableDef()
        from api.handlers import ping
        from api.handlers import zxcvbn
        self.app: web.Application() = web.Application()
        self.app.add_routes(self.routes)

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
        try:
            web.run_app(self.app, port=self.web_port, print=None)
        finally:
            self.logger.info("Goodbye!")
