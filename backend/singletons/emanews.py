import asyncio
import logging

import aiomysql
from aiohttp import web

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

        self.app: web.Application = None
        self.db: aiomysql.Pool = None
        self.setup_web_app()

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
            maxsize=self.db_pool_maxsize
        )

    def setup_web_app(self):
        """
        Imposta le routes dell'app aiohttp

        :return:
        """
        from api.handlers import ping
        self.app: web.Application() = web.Application()
        self.app.add_routes([
            web.get("/api/v1/ping", ping.handle)
        ])

    def start(self):
        """
        Avvia l'app aiohttp dell'API

        :return:
        """
        self.logger.info("Starting fitoemanews...")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connect_db())
        self.logger.info("Web API listening on {}:{}".format(self.web_host, self.web_port))
        web.run_app(self.app, port=self.web_port, print=None)
