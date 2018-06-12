import logging
from collections import namedtuple
from typing import Sequence, List

from aiohttp import web
from aiohttp.web_request import Request
from aiomysql import SSDictCursor
from schema import Optional, And, Use, Or

import api
from api.sessions import Session
from singletons.emanews import EmaNews


@api.base
@api.protected()
@api.args({
    Optional('query', default=''): And(str, Use(str.strip)),
    Optional('fetch_documents', default=True): Or(
        bool,
        And(str, Use(lambda x: x.lower().strip() in ('true', '1')))
    ),
    Optional('limit', default=0): Use(int, lambda x: x >= 0)
})
async def handle(request: Request, *, session: Session, params):
    herbs = []

    filters: List[str] = []
    if params["query"]:
        params["query"] = "%{}%".format(params["query"])
        filters.append("({})".format(
            " OR ".join(["{} LIKE %(query)s".format(x) for x in ('latin_name', 'botanic_name', 'english_name')])
        ))

    filters_string = " AND ".join(filters)

    async with EmaNews().db.acquire() as conn:
        async with conn.cursor(SSDictCursor) as cur:
            q = "SELECT * FROM herbs {} {}".format(
                    "WHERE {}".format(filters_string) if filters_string else "",
                    "LIMIT %(limit)s" if params["limit"] else ""
                )
            logging.debug(q)
            logging.debug(params)
            await cur.execute(q, {**params})
            while True:
                herbs_chunk = await cur.fetchmany()
                if not herbs_chunk:
                    break

                for herb in herbs_chunk:
                    if params["fetch_documents"]:
                        async with EmaNews().db.acquire() as doc_conn:
                            async with doc_conn.cursor() as doc_cur:
                                await doc_cur.execute("SELECT * FROM documents WHERE herb_id = %s", (herb["id"],))
                                herb["documents"] = await doc_cur.fetchall()
                    herbs.append(herb)
    return web.json_response({
        "herbs": herbs
    })
