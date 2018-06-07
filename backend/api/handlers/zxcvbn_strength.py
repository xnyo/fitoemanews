from aiohttp import web
from aiohttp.web_request import Request
from schema import And
from zxcvbn import zxcvbn

import api
from singletons.emanews import EmaNews

emanews = EmaNews()


@emanews.routes.get("/api/v1/zxcvbn")
@api.base
@api.args({
    "input": And(str, lambda x: x)
})
async def handle(request: Request, data):
    result = zxcvbn(data["input"])
    return web.json_response({
        "strength": (100 * result["score"]) / 4
    })
