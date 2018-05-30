import pytest
from aiohttp import web

from api.handlers import ping
import tests.unit_api.base

import tests.unit_api.errors


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


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    app.router.add_get("/api/v1/ping", ping.handle)
    return loop.run_until_complete(aiohttp_client(app))
