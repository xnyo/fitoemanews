import logging
from typing import List

from aiohttp import web
from aiohttp.web_request import Request
from aiomysql import SSDictCursor
from schema import Optional, And

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

    # Condizioni WHERE
    filters: List[str] = []
    if params["query"]:
        # WHERE per query ricerca
        params["query"] = "%{}%".format(params["query"])
        filters.append("({})".format(
            " OR ".join(["{} LIKE %(query)s".format(x) for x in ('latin_name', 'botanic_name', 'english_name')])
        ))

    # Join AND delle condizioni del WHERE
    filters_string = " AND ".join(filters)

    # Clausola LIMIT
    if not params["limit"]:
        # No LIMIT
        limit = ""
    elif params["limit"] and not params["page"]:
        # LIMIT senza pagina
        limit = "LIMIT {}".format(params["limit"])
    else:
        # LIMIT con pagina
        limit = "LIMIT {}, {}".format(params["page"] * params["limit"], params["limit"])

    # Costruisci due query identiche (results_query e count_query)
    # per prendere i risultati che rispecchiano gli argomenti forniti
    # e i risultati totali (query necessaria poichè è possibile implementare la clausola LIMIT)
    results_query, count_query = [
        "SELECT {what} FROM herbs {where} {order_by} ".format(
            what=x,
            where="WHERE {}".format(filters_string) if filters_string else "",
            order_by="ORDER BY {} {}".format(params["order_by"], params["direction"])
        ) for x in ("*", "COUNT(*) AS count")
    ]

    # Aggiunti il LIMIT nella query dei risultati DOPO la comprehension
    # in questo modo count_query non ha la clausola LIMIT
    results_query += limit

    # Prima connessione con SSDictCursor (per prendere X righe alla volta e non tutte le righe insieme,
    # in questo modo si riduce notevolmente l'uso di memoria durante l'esecuzione della query quando
    # ci sono query che ritornano molte righe)
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor(SSDictCursor) as cur:
            logging.debug(results_query)
            logging.debug(params)
            await cur.execute(results_query, {**params})

            # Recupera tutti i chunk
            while True:
                herbs_chunk = await cur.fetchmany()
                if not herbs_chunk:
                    break

                # Per ogni erba nel chunk...
                for herb in herbs_chunk:
                    # ...recupera i documenti se richiesto
                    if params["fetch_documents"]:
                        # Nuova connessione (DictCursor classico, poichè i documenti per ogni erba sono pochi)
                        async with EmaNews().db.acquire() as doc_conn:
                            async with doc_conn.cursor() as doc_cur:
                                await doc_cur.execute("SELECT * FROM documents WHERE herb_id = %s", (herb["id"],))
                                herb["documents"] = await doc_cur.fetchall()

                    # Aggiungi l'erba + documenti alla lista totale delle erbe
                    herbs.append(herb)

    # Determina il numero totale di righe
    if not limit:
        # Se non c'è la clausola LIMIT, il numero totale di risultati è uguale
        # alla lunghezza di total_herbs
        total_herbs = len(herbs)
    else:
        # Altrimenti, apri una nuova connessione ed esegui count_query
        # (uguale alla query per il fetch dei risultati, ma senza clausola
        # LIMIT e con SELECT COUNT(*) invece che SELECT *
        async with EmaNews().db.acquire() as conn:
            async with conn.cursor() as cur:
                logging.debug(count_query)
                await cur.execute(count_query, {**params})
                total_herbs = await cur.fetchone()
                if not total_herbs:
                    total_herbs = 0
                else:
                    total_herbs = total_herbs["count"]

    # Ritorna il risultato al client HTTP
    return web.json_response({
        "herbs": herbs,
        "total": total_herbs
    })
