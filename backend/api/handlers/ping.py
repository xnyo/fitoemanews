from aiohttp import web
from aiohttp.web_request import Request

import api
from singletons.emanews import EmaNews


@api.base
async def handle(request: Request):
    return web.json_response({
        "message": "ok",
        "version": EmaNews().VERSION
    })
