from singletons.emanews import EmaNews


async def test_smoke_scraper(cli):
    import jobs.scraper
    await jobs.scraper.scrape_herbs()
    await jobs.scraper.scrape_documents()
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT COUNT(*) AS c FROM herbs")
            assert (await cur.fetchone())["c"] > 1
            await cur.execute("SELECT COUNT(*) AS c FROM documents")
            assert (await cur.fetchone())["c"] > 1
