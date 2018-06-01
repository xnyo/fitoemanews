from aiohttp import web
from aiohttp.web_request import Request
from schema import Use, Schema

import api


@api.base
async def ping_handler(request: Request):
    return web.json_response({
        "message": "ok"
    })


@api.base
@api.args({
    "value": Use(int)
})
async def one_int_handler(request: Request, data):
    return web.json_response({
        "message": "ok",
        "value": data["value"]
    })


@api.base
@api.args({
    "a": Use(int),
    "b": Use(int)
})
async def sum_handler(request: Request, data):
    return web.json_response({
        "message": "ok",
        "result": data["a"] + data["b"]
    })


@api.base
@api.args(Schema(
    {"a": str}
))
async def premade_schema(request: Request, data):
    return web.json_response({
        "message": "ok",
        "result": data["a"]
    })
