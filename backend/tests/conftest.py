import asyncio

import aiomysql
import pytest
from aiohttp import web

import tests.unit_api.base

import tests.unit_api.errors
from migrator.migrator import Migrator
from singletons.config import Config
from singletons.emanews import EmaNews


@pytest.fixture
def unit_cli(loop, aiohttp_client):
    app = web.Application()
    app.router.add_get("/api/v1/ping", tests.unit_api.base.ping_handler)
    app.router.add_get("/api/v1/one_int", tests.unit_api.base.one_int_handler)
    app.router.add_post("/api/v1/sum", tests.unit_api.base.sum_handler)
    for code in (404, 500, 403, 409, 406, 201, 401):
        app.router.add_get("/api/v1/{}".format(code), getattr(tests.unit_api.errors, "e{}".format(code)))
    app.router.add_get("/api/v1/asyncio_cancelled", tests.unit_api.errors.asyncio_cancelled)
    app.router.add_get("/api/v1/unhandled_error", tests.unit_api.errors.unhandled_error)
    app.router.add_get("/api/v1/premade_schema", tests.unit_api.base.premade_schema)
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture(scope="session", autouse=True)
def drop_all_tables():
    async def do():
        c = Config()
        async with aiomysql.connect(
            host=c["DB_HOST"],
            port=c["DB_PORT"],
            user=c["DB_USERNAME"],
            password=c["DB_PASSWORD"],
            db=c["TEST_DB_NAME"]
        ) as conn:
            cur = await conn.cursor()
            await cur.execute(
                "SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s", (c["TEST_DB_NAME"],)
            )
            tables = await cur.fetchall()
            await cur.execute("SET FOREIGN_KEY_CHECKS = 0")
            for table, in tables:
                await cur.execute("DROP TABLE {}".format(table,))
            await cur.execute("SET FOREIGN_KEY_CHECKS = 1")
            await conn.commit()

    asyncio.get_event_loop().run_until_complete(do())


@pytest.fixture(scope="session", autouse=True)
def app(drop_all_tables):
    """
    Fixtrure eseguita una sola volta all'avvio della sessione.
    Crea il singleton EmaNews e ritorna l'app aiohttp

    :return:
    """
    c = Config()
    server = EmaNews(
        db_host=c["DB_HOST"],
        db_port=c["DB_PORT"],
        db_username=c["DB_USERNAME"],
        db_password=c["DB_PASSWORD"],
        db_database=c["TEST_DB_NAME"],
        db_pool_minsize=c["DB_POOL_MIN_SIZE"],
        db_pool_maxsize=c["DB_POOL_MAX_SIZE"],
        debug=False
    )
    server.initialize()
    yield server.app


@pytest.fixture
def cli(loop, aiohttp_client, app):
    return loop.run_until_complete(aiohttp_client(app))
