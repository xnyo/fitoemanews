async def get_herb(cur, herb_id):
    await cur.execute("SELECT * FROM herbs WHERE id = %s LIMIT 1", (herb_id,))
    return await cur.fetchone()


async def get_document(cur, document_id):
    await cur.execute("SELECT * FROM documents JOIN herbs ON documents.herb_id = herbs.id "
                      "WHERE documents.id = %s LIMIT 1", (document_id,))
    return await cur.fetchone()
