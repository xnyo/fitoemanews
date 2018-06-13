import time

from aiohttp import web
from aiohttp.web_request import Request

import api
from api.sessions import Session
from exceptions.api import NotAcceptableError
from singletons.emanews import EmaNews
from utils import general


@api.base
@api.protected()
async def get(request: Request, *, session: Session):
    token = ""

    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT telegram_user_id FROM users WHERE id = %s LIMIT 1",
                (session.user_id,)
            )
            telegram_user_id = await cur.fetchone()
            if telegram_user_id["telegram_user_id"] is not None:
                raise NotAcceptableError("Account già collegato con Telegram")

            await cur.execute(
                "DELETE FROM telegram_link_tokens WHERE user_id = %s AND `expire` < UNIX_TIMESTAMP()",
                (session.user_id,)
            )
            await conn.commit()

            await cur.execute(
                "SELECT token FROM telegram_link_tokens WHERE user_id = %s AND `expire` > UNIX_TIMESTAMP() LIMIT 1",
                (session.user_id,)
            )
            token = await cur.fetchone()
            if token is None:
                found = False
                while not found:
                    token = general.random_string_secure(16)
                    await cur.execute("SELECT id FROM telegram_link_tokens WHERE token = %s LIMIT 1", (token,))
                    found = not await cur.fetchone()
                await cur.execute(
                    "INSERT INTO telegram_link_tokens (token, user_id, `expire`) VALUES (%s, %s, %s)",
                    (token, session.user_id, int(time.time()) + 3600)
                )
            else:
                token = token["token"]
            await conn.commit()

    # Ok!
    return web.json_response({
        "telegram_link": "https://telegram.me/{}?start={}".format("emanewsbot", token)
    })


@api.base
@api.protected()
async def delete(request: Request, *, session: Session):
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE users SET telegram_user_id = NULL WHERE id = %s LIMIT 1", (session.user_id,))
            await conn.commit()
    return web.json_response({
        "message": "ok"
    })
