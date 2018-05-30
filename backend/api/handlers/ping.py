from aiohttp import web
from aiohttp.web_request import Request
from schema import Use

import api


@api.base
async def handle(request: Request):
    return web.json_response({
        "message": "ok"
    })
