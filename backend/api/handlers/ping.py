from aiohttp import web
from aiohttp.web_request import Request

import api


@api.base
async def handle(request: Request):
    return web.json_response({
        "message": "ok"
    })


# @api.base
# @api.args({
#     "a": Use(int),
#     "b": Use(int)
# })
# async def handle_test(request, data):
#     return web.json_response({
#         "res": data["a"] + data["b"]
#     })
