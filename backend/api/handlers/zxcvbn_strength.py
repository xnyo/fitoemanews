from aiohttp import web
from aiohttp.web_request import Request
from schema import And
from zxcvbn import zxcvbn

import api


@api.base
@api.args({
    "input": And(str, lambda x: x, error="Input non valido")
})
async def handle(request: Request, *, params):
    result = zxcvbn(params["input"])
    return web.json_response({
        "strength": (100 * result["score"]) / 4
    })
