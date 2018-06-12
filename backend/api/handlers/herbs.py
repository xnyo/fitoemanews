from aiohttp import web
from aiohttp.web_request import Request
from aiomysql import SSDictCursor

import api
from api.sessions import Session
from singletons.emanews import EmaNews


@api.base
@api.protected()
async def handle(session: Session, request: Request):
    herbs = []

    async with EmaNews().db.acquire() as conn:
        async with conn.cursor(SSDictCursor) as cur:
            await cur.execute("SELECT * FROM herbs")
            while True:
                herbs_chunk = await cur.fetchmany()
                if not herbs_chunk:
                    break
                for herb in herbs_chunk:
                    async with EmaNews().db.acquire() as doc_conn:
                        async with doc_conn.cursor() as doc_cur:
                            await doc_cur.execute("SELECT * FROM documents WHERE herb_id = %s", (herb["id"],))
                            herb["documents"] = await doc_cur.fetchall()
                    herbs.append(herb)
    return web.json_response({
        "herbs": herbs
    })
