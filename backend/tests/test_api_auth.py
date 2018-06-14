from tests.conftest import login


async def test_protected_not_logged_in(cli):
    resp = await cli.get("/api/v1/herbs")
    assert resp.status == 401
    data = await resp.json()
    assert data["message"] == "Not authenticated"


async def test_protected_logged_in_cookie(cli):
    await login(cli)
    resp = await cli.get("/api/v1/herbs")
    assert resp.status == 200


async def test_protected_logged_in_api_key_header(cli):
    resp = await cli.get("/api/v1/herbs", headers={
        "X-EmaNews-Token": "testtoken"
    })
    assert resp.status == 200


async def test_protected_invalid_api_token(cli):
    resp = await cli.get("/api/v1/herbs", headers={
        "X-EmaNews-Token": "invalid"
    })
    assert resp.status == 403


async def test_protected_no_cookie_no_key(cli):
    resp = await cli.get("/api/v1/herbs")
    assert resp.status == 401
