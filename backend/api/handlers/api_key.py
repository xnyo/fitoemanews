from aiohttp import web
from aiohttp.web_request import Request

import api
from api.schema import StrippedString
from api.sessions import Session
from singletons.emanews import EmaNews
from utils import general


@api.base
@api.protected()
@api.args({
    "name": StrippedString
})
async def post(request: Request, *, session: Session, params):
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            found = False
            while not found:
                key = general.random_string_secure(32)
                key_hash = general.sha512(key)
                await cur.execute("SELECT id FROM api_keys WHERE key_hash = %s LIMIT 1", (key_hash,))
                found = not await cur.fetchone()
            await cur.execute(
                "INSERT INTO api_keys (name, key_hash, user_id) VALUES (%s, %s, %s)",
                (params["name"], key_hash, session.user_id)
            )
            await conn.commit()
    return web.json_response({
        "message": "ok",
        "key": key
    })


@api.base
@api.protected()
async def get(request: Request, *, session: Session):
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT id, name FROM api_keys WHERE user_id = %s", (session.user_id,))
            results = await cur.fetchall()
    return web.json_response(results)


@api.base
@api.protected()
async def delete(request: Request, *, session: Session):
    id_ = request.match_info["id_"].strip()
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM api_keys WHERE id = %s AND user_id = %s LIMIT 1", (id_, session.user_id,))
            await conn.commit()
    return web.json_response({
        "message": "ok"
    })
