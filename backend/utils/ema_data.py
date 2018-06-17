from typing import Optional

from aiomysql import Cursor


async def get_herb(cur: Cursor, herb_id: int) -> Optional[dict]:
    """
    Ritorna le informazioni di un'erba dal db

    :param cur: cursore aiomysql
    :param herb_id: id erba
    :return: informazioni erba
    """
    await cur.execute("SELECT * FROM herbs WHERE id = %s LIMIT 1", (herb_id,))
    return await cur.fetchone()


async def get_document(cur: Cursor, document_id: int) -> Optional[dict]:
    """
    Ritorna le informazioni di un documento e di un'erba dal db

    :param cur: cursore aiomysql
    :param document_id: id documento
    :return: informazioni documento e relativa erba
    """
    await cur.execute("SELECT * FROM documents JOIN herbs ON documents.herb_id = herbs.id "
                      "WHERE documents.id = %s LIMIT 1", (document_id,))
    return await cur.fetchone()
