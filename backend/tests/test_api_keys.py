from singletons.emanews import EmaNews
from tests.conftest import login

key = ""

async def test_list_api_keys_not_logged_in(cli):
    resp = await cli.get("/api/v1/api_keys")
    assert resp.status == 401


async def test_list_api_keys_empty(cli):
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM api_keys WHERE id > 1")   # id = 1 api key additional.sql
            await conn.commit()
    await login(cli)
    resp = await cli.get("/api/v1/api_keys")
    assert resp.status == 200
    data = await resp.json()
    assert len(data["keys"]) == 1


async def test_create_api_key(cli):
    global key
    await login(cli)
    resp = await cli.post("/api/v1/api_keys", json={
        "name": "test"
    })
    assert resp.status == 200
    data = await resp.json()
    key = data["key"]
    assert "key" in data and type(data["key"]) is str and data["key"]


async def test_list_api_keys_again(cli):
    await login(cli)
    resp = await cli.get("/api/v1/api_keys")
    assert resp.status == 200
    data = await resp.json()
    assert len(data["keys"]) == 2 and data["keys"][0]["name"] == "test"


async def test_newly_created_api_key(cli):
    resp = await cli.get("/api/v1/herbs", params={
        "apikey": key
    })
    assert resp.status == 200


async def test_delete_api_key(cli):
    await login(cli)
    resp = await cli.get("/api/v1/api_keys")
    assert resp.status == 200
    data = await resp.json()
    key_id = data["keys"][1]["id"]

    resp = await cli.delete("/api/v1/api_keys/{}".format(key_id))
    assert resp.status == 200


async def test_deleted_api_key(cli):
    resp = await cli.get("/api/v1/herbs", params={
        "apikey": key
    })
    assert resp.status == 403
