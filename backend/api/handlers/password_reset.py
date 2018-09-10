import logging

import bcrypt

from aiohttp import web
from aiohttp.web_request import Request

import api
from api.schema import Password
from exceptions.api import NotFoundError
from singletons.emanews import EmaNews


@api.base
@api.guest_only
@api.args({"password": Password})
async def post(request: Request, *, params):
    token = request.match_info["token"].strip()
    logging.debug("Resetting password for recovery token {}".format(token))

    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            # Recupera utente da token
            await cur.execute(
                "SELECT users.id FROM users JOIN password_reset_tokens ON users.id = password_reset_tokens.user_id "
                "WHERE token = %s AND privileges & 2 > 0 AND `expire` > UNIX_TIMESTAMP() LIMIT 1",
                (token,)
            )
            db_user = await cur.fetchone()
            if not db_user:
                raise NotFoundError("Token non valido o scaduto.")

            # Cripta nuova password
            bcrypted_password = bcrypt.hashpw(params["password"], bcrypt.gensalt())

            # Aggiorna db
            await cur.execute(
                "UPDATE users SET password = %s WHERE id = %s LIMIT 1",
                (bcrypted_password, db_user["id"])
            )
            await cur.execute("DELETE FROM password_reset_tokens WHERE token = %s LIMIT 1", (token,))
            await conn.commit()

    # Ok!
    return web.json_response({
        "message": "ok"
    })


@api.base
@api.guest_only
async def get(request: Request):
    token = request.match_info["token"].strip()
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT id FROM password_reset_tokens WHERE token = %s AND `expire` > UNIX_TIMESTAMP() LIMIT 1",
                (token,)
            )
            if await cur.fetchone():
                return web.json_response({"message": "ok"})
            raise NotFoundError("Token invalido o scaduto.")