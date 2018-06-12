import bcrypt
from aiohttp import web
from aiohttp.web_request import Request
from schema import And, Use

import api
from api.sessions import Session, SessionFactory
from constants.privileges import Privileges
from exceptions.api import NotFoundError, ForbiddenError
from singletons.emanews import EmaNews


@api.base
@api.guest_only
@api.args({
    "email": str,
    "password": And(
        str,
        Use(lambda x: x.encode())
    )
})
async def handle(request: Request, *, params):
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM users WHERE email = %s LIMIT 1", (params["email"],))
            db_user = await cur.fetchone()
            if not db_user:
                raise NotFoundError("L'indirizzo email inserito non è associato a nessun account")
            if not bcrypt.checkpw(params["password"], db_user["password"]):
                raise ForbiddenError("La password inserita è errata")
            if db_user["privileges"] & Privileges.PENDING_ACTIVATION:
                raise ForbiddenError("L'account non è ancora stato attivato. Per favore, controlla la tua casella "
                                     "di posta elettronica e clicca sul link che hai ricevuto per verificare "
                                     "il tuo account.")

    session = await SessionFactory.new_session(db_user["id"])
    resp = web.json_response({
        "message": "ok"
    })
    resp.set_cookie("session", session.token, max_age=Session.SESSION_EXPIRE_TIME)  #, secure=True)
    return resp
