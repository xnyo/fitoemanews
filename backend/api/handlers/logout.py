from aiohttp.web_request import Request

import api
from api.sessions import Session, RedisSession
from exceptions.api import ForceLogoutError, NotAcceptableError


@api.base
@api.protected()
async def handle(request: Request, *, session: Session):
    if type(session) is not RedisSession:
        raise NotAcceptableError("Can't logout.")
    await session.destroy()
    raise ForceLogoutError("ok")
