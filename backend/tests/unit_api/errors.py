import asyncio

from aiohttp.web_request import Request

import api
from exceptions.api import NotFoundError, InternalServerError, ForbiddenError, ConflictError, NotAcceptableError, \
    Created, NotAuthenticatedError


@api.base
async def e404(request: Request):
    raise NotFoundError()


@api.base
async def e500(request: Request):
    raise InternalServerError()


@api.base
async def e403(request: Request):
    raise ForbiddenError()


@api.base
async def e409(request: Request):
    raise ConflictError()


@api.base
async def e406(request: Request):
    raise NotAcceptableError()


@api.base
async def e201(request: Request):
    raise Created()


@api.base
async def e401(request: Request):
    raise NotAuthenticatedError()


@api.base
async def asyncio_cancelled(request: Request):
    raise asyncio.CancelledError()


@api.base
async def unhandled_error(request: Request):
    a = 1/0
