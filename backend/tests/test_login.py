from tests.conftest import login


async def test_login_missing_all_fields(cli):
    resp = await cli.post("/api/v1/login")
    assert resp.status == 400


async def test_login_missing_some_fields(cli):
    fields = ["email", "password"]
    for field in fields:
        resp = await cli.post("/api/v1/login", json={
            field: "gibberish"
        })
        assert resp.status == 400


async def test_login_valid(cli):
    resp = await cli.post("/api/v1/login", json={
        "email": "user@emane.ws",
        "password": "password"
    })
    assert resp.status == 200


async def test_login_wrong_email(cli):
    resp = await cli.post("/api/v1/login", json={
        "email": "invalid@emane.ws",
        "password": "password"
    })
    assert resp.status == 404
    data = await resp.json()
    assert data["message"].startswith("L'indirizzo email inserito non")


async def test_login_wrong_password(cli):
    resp = await cli.post("/api/v1/login", json={
        "email": "user@emane.ws",
        "password": "ops"
    })
    assert resp.status == 403
    data = await resp.json()
    assert data["message"] == "La password inserita è errata"


async def test_login_pending_activation(cli):
    resp = await cli.post("/api/v1/login", json={
        "email": "pending@emane.ws",
        "password": "password"
    })
    assert resp.status == 403
    data = await resp.json()
    assert data["message"].startswith("L'account non è ancora stato attivato")


async def test_login_already_logged_in(cli):
    await login(cli)
    resp = await cli.post("/api/v1/login", json={
        "email": "user@emane.ws",
        "password": "password"
    })
    assert resp.status == 403
    data = await resp.json()
    assert data["message"] == "You are already logged in"
