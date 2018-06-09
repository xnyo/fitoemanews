import bcrypt
from aiohttp import web
from aiohttp.web_request import Request

import api
from constants.privileges import Privileges
from exceptions.api import NotFoundError
from singletons.emanews import EmaNews


@api.base
async def handle(request: Request):
    token = request.match_info["token"].strip()

    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT id, user_id FROM activation_tokens WHERE token = %s LIMIT 1", (token,))
            db_token = await cur.fetchone()
            if not db_token:
                raise NotFoundError("Token attivazione non valido")
            await cur.execute("DELETE FROM activation_tokens WHERE id = %s LIMIT 1", (db_token["id"],))
            await cur.execute("UPDATE users SET privileges = %s WHERE id = %s LIMIT 1",
                              (int(Privileges.NORMAL), db_token["user_id"]))
            await conn.commit()

    # Ok!
    return web.json_response({
        "message": "ok"
    })
