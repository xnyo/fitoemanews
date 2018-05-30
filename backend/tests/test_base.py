async def test_ping(cli):
    resp = await cli.get("/api/v1/ping")
    assert resp.status == 200
    assert (await resp.json())["message"] == "ok"
