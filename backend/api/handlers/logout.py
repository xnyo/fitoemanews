from aiohttp.web_request import Request

import api
from api.sessions import Session
from exceptions.api import ForceLogoutError


@api.base
@api.protected()
async def handle(session: Session, request: Request):
    await session.destroy()
    raise ForceLogoutError("ok")
