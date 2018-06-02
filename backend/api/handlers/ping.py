from aiohttp import web
from aiohttp.web_request import Request

from singletons.emanews import EmaNews

emanews = EmaNews()


@emanews.routes.get('/api/v1/public/ping')
async def handle(request: Request):
    return web.json_response({
        "message": "ok"
    })
