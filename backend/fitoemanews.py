import asyncio
import logging
from collections import namedtuple

import aiohttp
import time

import aiomysql
from lxml import html

from singletons.config import Config
from singletons.db import Db

# TODO: Spostare in costanti
EMA_URL = "http://www.ema.europa.eu/ema/index.jsp?searchType=Latin+name+of+herbal+substance&curl=pages%2Fmedicines%2F" \
          "landing%2Fherbal_search.jsp&treeNumber=&searchkwByEnter=false&mid=&taxonomyPath=&keyword=Enter+keywords&al" \
          "readyLoaded=true&startLetter=View+all"

# TODO: Spostare
EmaDocument = namedtuple("EmaDocument", ["name", "type", "url", "language", "first_published", "last_updated"])
# TODO: EmaHerb = namedtuple("EmaHerb", [...])


# TODO: Spostare in exceptions
class NonOkResponseError(Exception):
    pass


class InvalidHerbError(Exception):
    pass


class InvalidDocumentError(Exception):
    pass


async def scrape_herbs():
    page = 1
    processed_elements = 0

    async with aiohttp.ClientSession() as session:
        # Continua a fare lo scraping se nella pagina attuale ci sono elementi
        while processed_elements > 0 or page == 1:
            # Reset variabili
            processed_elements = 0

            try:
                async with session.get("{}&pageNo={}".format(EMA_URL, page)) as resp:
                    logging.info("Scraping page {}".format(page))
                    if resp.status != 200:
                        raise NonOkResponseError()

                    # Parse HTML
                    tree = html.fromstring(await resp.text())

                    # Processa ogni riga della tabella
                    for table_row in tree.xpath(".//div[@id='searchResults']//table/tbody/tr"):
                        # TODO: func
                        # Il nome latino è un `th` con `a` all'interno
                        latin_name_anchor = table_row.xpath("./th/a")

                        # Se non è presente, non considerare questo elemento
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
                        if status not in ["R", "C", "D", "P", "PF", "F"]:
                            raise InvalidHerbError("Status is invalid ({}), element skipped".format(status))

                        # TODO: Namedtuple

                        # Salvataggio nel db
                        async with Db().acquire() as conn:
                            async with conn.cursor() as cur:
                                # Controllo se l'erba esiste già nel database
                                await cur.execute("SELECT id FROM herbs WHERE latin_name = %s LIMIT 1", (latin_name,))

                                if await cur.fetchone() is None:
                                    # Se non esiste, aggiungila
                                    await cur.execute(
                                        "INSERT INTO herbs (latin_name, botanic_name, english_name, status, url, "
                                        "latest_update) VALUES (%s, %s, %s, %s, %s, %s)",
                                        (latin_name, botanic_name, english_name, status, url, int(time.time()))
                                    )
                                    await conn.commit()

                                # TODO: Aggiornamento?
                        processed_elements += 1

                    print("Processed {} elements".format(processed_elements))
                    page += 1
            except InvalidHerbError as e:
                logging.warning(e)


async def scrape_documents():
    def scrape_table(path, type_):
        results = []
        for document in tree.xpath(path):
            columns = document.xpath("td")
            if len(columns) != 4:
                raise InvalidDocumentError(
                    "Row has {} elements instead of 3, element skipped".format(len(columns))
                )
            document_a = columns[0].find("a")
            name = document_a.text_content().strip()
            url = "http://www.ema.europa.eu/{}".format(document_a.get("href").lstrip("/"))
            language, first_published, last_updated = [x.text.strip() for x in columns[1:]]
            print(url, name, language, first_published, last_updated)
            results.append(
                EmaDocument(name, type_, url, language, first_published, last_updated)
            )
        return results

    # Seleziona tutte le erbe dal db
    async with Db().acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM herbs")
            herbs = await cur.fetchall()

    async with aiohttp.ClientSession() as session:
        for herb in herbs:
            # Scraping della pagina del sito dell'EMA per ogni erba
            async with session.get(herb["url"]) as resp:
                tree = html.fromstring(await resp.text())
                consultations = scrape_table(".//div[@id='consultation']//table/tbody/tr", "consultation")
                other_documents = scrape_table(".//div[@id='documents']//table/tbody/tr", "other_document")
                for document in consultations + other_documents:
                    # TODO: db
                    pass


async def dispose():
    # Chiudi pool mysql
    Db().close()
    await Db().wait_closed()


def main():
    print("Fitoemanews POC")
    loop = asyncio.new_event_loop()
    c = Config()
    loop.run_until_complete(
        Db().create(
            host=c["DB_HOST"],
            user=c["DB_USERNAME"],
            password=c["DB_PASSWORD"],
            db=c["DB_NAME"],
            charset="utf8",
            use_unicode=True,
            cursorclass=aiomysql.DictCursor,
            loop=loop,
        )
    )
    try:
        s = int(input("1: erbe\n2: documenti\n\n> "))
        loop.run_until_complete([scrape_herbs, scrape_documents][s + 1]())
    except KeyboardInterrupt:
        logging.info("Interrupted.")
    finally:
        loop.run_until_complete(dispose())
        loop.close()


if __name__ == "__main__":
    main()
