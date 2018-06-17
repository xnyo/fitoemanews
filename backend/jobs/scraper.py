import asyncio
import itertools
from typing import Iterable, Awaitable, Coroutine, Callable, List, Tuple

from aiomysql import SSDictCursor
from apscheduler.triggers.interval import IntervalTrigger

from constants.notifications import NotificationWhen
from singletons.emanews import EmaNews

import logging

import aiohttp
import time

from lxml import html

from utils import notificator, ema_data
from utils.ema import EmaDocument

emanews = EmaNews()
logger = logging.getLogger("scraper")

# TODO: Spostare in costanti
EMA_URL = "http://www.ema.europa.eu/ema/index.jsp?searchType=Latin+name+of+herbal+substance&curl=pages%2Fmedicines%2F" \
          "landing%2Fherbal_search.jsp&treeNumber=&searchkwByEnter=false&mid=&taxonomyPath=&keyword=Enter+keywords&al" \
          "readyLoaded=true&startLetter=View+all"


class NonOkResponseError(Exception):
    pass


class InvalidHerbError(Exception):
    pass


class InvalidDocumentError(Exception):
    pass


async def scrape_herbs():
    """
    Effettua lo scraping delle erbe dal sito dell'EMA

    :return:
    """
    page = 1
    processed_elements = 0

    async with aiohttp.ClientSession() as session:
        # Continua a fare lo scraping se nella pagina attuale ci sono elementi
        while processed_elements > 0 or page == 1:
            # Reset variabili pagina
            processed_elements = 0

            try:
                async with session.get("{}&pageNo={}".format(EMA_URL, page)) as resp:
                    logger.debug("Scraping page {}".format(page))
                    if resp.status != 200:
                        raise NonOkResponseError()

                    # Parse HTML
                    tree = html.fromstring(await resp.text())

                    # Processa ogni riga della tabella
                    for table_row in tree.xpath(".//div[@id='searchResults']//table/tbody/tr"):
                        # TODO: func
                        # Il nome latino è un `th` con `a` all'interno
                        latin_name_anchor = table_row.xpath("./th/a")

                        # Se non è presente il nome latino, non considerare questo elemento
                        if not latin_name_anchor:
                            raise InvalidHerbError("No anchor found, element skipped")

                        # Estrai `href` da `a` e costruisci URL
                        url = "http://www.ema.europa.eu/ema/{}".format(latin_name_anchor[0].get("href").lstrip("/"))

                        # Nome latino
                        latin_name = latin_name_anchor[0].text.strip()

                        # Testo restanti 3 colonne (potrebbero contenere dei tag con `i`)
                        columns_text = [x.text_content().strip() for x in table_row.xpath("./td")]

                        # Se non ci sono esattamente 3 colonne extra, non considerare questo elemento
                        if len(columns_text) != 3:
                            raise InvalidHerbError(
                                "Row has {} elements instead of 3, element skipped".format(len(columns_text))
                            )

                        # Estrai le informazioni dalle altre colonne
                        botanic_name, english_name, status = columns_text

                        # Controllo validità status
                        if status not in ("R", "C", "D", "P", "PF", "F"):
                            raise InvalidHerbError("Status is invalid ({}), element skipped".format(status))

                        # TODO: Namedtuple

                        # Salvataggio nel db
                        async with emanews.db.acquire() as conn:
                            async with conn.cursor() as cur:
                                # Controllo se l'erba esiste già nel database
                                await cur.execute(
                                    "SELECT id, status FROM herbs WHERE latin_name = %s LIMIT 1",
                                    (latin_name,)
                                )
                                herb = await cur.fetchone()

                                if herb is None:
                                    # Se non esiste, aggiungila
                                    await cur.execute(
                                        "INSERT INTO herbs (latin_name, botanic_name, english_name, status, url, "
                                        "latest_update) VALUES (%s, %s, %s, %s, %s, %s)",
                                        (latin_name, botanic_name, english_name, status, url, int(time.time()))
                                    )
                                    await conn.commit()
                                    await notificator.notify(
                                        NotificationWhen.NEW_MEDICINE,
                                        await ema_data.get_herb(cur, cur.lastrowid)
                                    )
                                elif herb["status"] != status:
                                    # Cambio stato
                                    await cur.execute(
                                        "UPDATE herbs SET status = %s, latest_update = %s WHERE id = %s LIMIT 1",
                                        (status, int(time.time()), herb["id"])
                                    )
                                    await conn.commit()
                                    await notificator.notify(
                                        NotificationWhen.MEDICINE_UPDATE,
                                        await ema_data.get_herb(cur, herb["id"]),
                                        herb["id"]
                                    )

                                # TODO: Aggiornamento?
                        processed_elements += 1

                    logger.debug("Processed {} elements".format(processed_elements))
                    page += 1
            except InvalidHerbError as e:
                logger.warning(e)


async def scrape_documents():
    """
    Effettua lo scraping dei documenti dal sito dell'EMA, per ogni erba salvata nel database

    :return:
    """
    def scrape_table(rows_path: str, type_: str) -> Iterable[EmaDocument]:
        """
        Generatore che effettua lo scraping delle tabelle del sito dell'EMA contenenti documenti
        
        :param rows_path: xpath righe tabella
        :param type_: tipo dei documenti contenuti in questa tabella
        :return: oggetti `EmaDocument` che rappresentano i documenti presenti nella tabella
        """
        for doc in tree.xpath(rows_path):
            # Prendi tutte le colonne (devono essere 4)
            columns = doc.xpath("td")
            if len(columns) != 4:
                raise InvalidDocumentError(
                    "Row has {} elements instead of 3, element skipped".format(len(columns))
                )

            # Estrai tag `a` contenente nome e URL
            document_a = columns[0].find("a")

            # Estrai nome documento
            name = document_a.text_content().strip()

            # Determina URL documento
            url = "http://www.ema.europa.eu/{}".format(document_a.get("href").lstrip("/"))

            # Estrai altri dati
            language, first_published, last_updated = [x.text.strip() for x in columns[1:]]
            # logger.debug(("{} " * 5).format(url, name, language, first_published, last_updated))

            # Ritorna il documento
            yield EmaDocument(name, type_, url, language, first_published, last_updated)

    # Mantieni aperta una connessione al db
    async with emanews.db.acquire() as conn:
        async with conn.cursor(SSDictCursor) as unbuffered_cur:
            # Seleziona tutte le erbe dal db
            await unbuffered_cur.execute("SELECT * FROM herbs")

            # Apri sessione aiohttp
            async with aiohttp.ClientSession() as session:
                # Scraping documenti per ogni erba presente nel database
                # Il recupero delle erbe avviene con un unbuffered cursor
                for herb in await unbuffered_cur.fetchall():
                    logger.debug("Scraping documents for herb {}".format(herb["english_name"]))
                    # Apro un secondo cursore (buffered) da usare per leggere/modificare i documenti
                    async with conn.cursor() as cur:
                        # Recupera i documenti attualmente salvati per questa erba
                        await cur.execute("SELECT * FROM documents WHERE herb_id = %s", (herb["id"],))
                        stored_documents = [
                            {**x, **{"name": x["name"].strip().lower()}} for x in await cur.fetchall()
                        ]

                        # Scraping della pagina del sito dell'EMA di questa erba
                        async with session.get(herb["url"]) as resp:
                            # Parsing HTML
                            tree = html.fromstring(await resp.text())

                            # Elabora ogni documento, sia nella scheda "consultations" che "other"
                            update_herb_latest_update = False
                            notifications: List[Tuple[NotificationWhen, int, int]] = []
                            for document in itertools.chain(
                                scrape_table(".//div[@id='consultation']//table/tbody/tr", "consultation"),
                                scrape_table(".//div[@id='documents']//table/tbody/tr", "other")
                            ):
                                # Controlla se esiste un documento con lo stesso nome
                                safe_document_name = document.name.strip().lower()
                                matching_document = next(
                                    (x for x in stored_documents
                                     if x["name"] == safe_document_name or x["url"] == document.url),
                                    None
                                )

                                if matching_document is None:
                                    # Nuovo documento
                                    update_herb_latest_update = True
                                    logging.debug("Adding {}".format(document))
                                    await cur.execute(
                                        "INSERT INTO documents (herb_id, type, name, language, "
                                        "first_published, last_updated_ema, url) VALUES "
                                        "(%s, %s, %s, %s, %s, %s, %s)",
                                        (
                                            herb["id"], document.type, document.name, document.language,
                                            document.first_published, document.last_updated_ema, document.url
                                        )
                                    )
                                    notifications.append((NotificationWhen.NEW_DOCUMENT, cur.lastrowid, herb["id"]))
                                elif (
                                    document.last_updated_ema is not None
                                    and matching_document["last_updated_ema"] is None
                                ) or (
                                    type(document.last_updated_ema) is int and
                                    type(matching_document["last_updated_ema"]) is int
                                    and document.last_updated_ema > matching_document["last_updated_ema"]
                                ):
                                    # Data aggiornamento presente (precedentemente mancante)
                                    # o superiore a quella salvata, aggiorna informazioni nel db
                                    update_herb_latest_update = True
                                    logging.debug("Updating {}".format(document))
                                    await cur.execute(
                                        "UPDATE documents SET type = %s, name = %s, language = %s,"
                                        "first_published = %s, last_updated_ema = %s, url = %s "
                                        "WHERE id = %s LIMIT 1",
                                        (
                                            document.type, document.name, document.language,
                                            document.first_published, document.last_updated_ema, document.url,
                                            matching_document["id"]
                                        )
                                    )
                                    notifications.append(
                                        (NotificationWhen.DOCUMENT_UPDATE, matching_document["id"], herb["id"])
                                    )
                            if update_herb_latest_update:
                                # Se abbiamo aggiunto/aggiornato un documento di questa erba,
                                # modifica anche la data di aggiornamento dell'erba
                                await cur.execute(
                                    "UPDATE herbs SET latest_update = IFNULL(("
                                    "  SELECT IFNULL(last_updated_ema, first_published) FROM documents "
                                    "  WHERE herb_id = %(herb_id)s"
                                    "  ORDER BY last_updated_ema, first_published DESC LIMIT 1"
                                    "), UNIX_TIMESTAMP()) WHERE id = %(herb_id)s LIMIT 1",
                                    {"herb_id": herb["id"]}
                                )

                            # Commit per ogni erba
                            await conn.commit()

                            # Notifiche
                            if notifications:
                                asyncio.gather(*[
                                    notificator.notify(
                                        when,
                                        await ema_data.get_document(cur, document_id),
                                        herb_id
                                    ) for when, document_id, herb_id in notifications
                                ])


@emanews.scheduler.scheduled_job(
    IntervalTrigger(minutes=10)
)
async def scrape_everything():
    """
    Effettua lo scraping delle erbe e dei documenti
    dal sito dell'EMA. Questa funzione è avviata
    ogni 10 minuti dallo schedulatore

    :return:
    """
    await scrape_herbs()
    logger.info("Herbs scraping completed")
    await scrape_documents()
    logger.info("Documents scraping completed")
