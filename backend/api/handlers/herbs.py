import logging
from collections import namedtuple
from typing import Sequence, List

from aiohttp import web
from aiohttp.web_request import Request
from aiomysql import SSDictCursor
from schema import Optional, And, Use, Or

import api
from api.schema import BooleanString, PositiveInteger, StrippedString
from api.sessions import Session
from singletons.emanews import EmaNews


@api.base
@api.protected()
@api.args({
    Optional("query", default=""): And(StrippedString, error="Query ricerca non valida"),
    Optional("fetch_documents", default=True): And(BooleanString, error="Valore fetch_documents non valido"),
    Optional("limit", default=50): And(PositiveInteger, error="Limit deve essere un intero positivo"),
    Optional("page", default=0): And(PositiveInteger, error="Page deve essere un intero positivo"),
    Optional("order_by", default="latin_name"): And(
        StrippedString, lambda x: x in ("latin_name", "botanic_name", "english_name", "status", "latest_update"),
        error="Valore order_by non valido"
    ),
    Optional("direction", default="asc"): And(
        StrippedString, lambda x: x.lower() in ("asc", "desc"),
        error="Direzione non valida"
    )
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
    if not params["limit"]:
        limit = ""
    elif params["limit"] and not params["page"]:
        limit = "LIMIT {}".format(params["limit"])
    else:
        limit = "LIMIT {}, {}".format(params["page"] * params["limit"], params["limit"])

    results_query, count_query = [
        "SELECT {what} FROM herbs {where} {order_by} ".format(
            what=x,
            where="WHERE {}".format(filters_string) if filters_string else "",
            order_by="ORDER BY {} {}".format(params["order_by"], params["direction"])
        ) for x in ("*", "COUNT(*) AS count")
    ]
    results_query += limit
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor(SSDictCursor) as cur:
            logging.debug(results_query)
            logging.debug(params)
            await cur.execute(results_query, {**params})
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

    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            logging.debug(count_query)
            await cur.execute(count_query, {**params})
            total_herbs = await cur.fetchone()
            if not total_herbs:
                total_herbs = 0
            else:
                total_herbs = total_herbs["count"]
    return web.json_response({
        "herbs": herbs,
        "total": total_herbs
    })
