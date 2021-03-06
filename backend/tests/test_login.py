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


async def test_logout(cli):
    await login(cli)
    resp = await cli.get("/api/v1/herbs")
    assert resp.status == 200
    resp = await cli.post("/api/v1/logout")
    assert resp.status == 200
    resp = await cli.get("/api/v1/herbs")
    assert resp.status == 401


async def test_logout_api_key(cli):
    resp = await cli.post("/api/v1/logout", params={
        "apikey": "testtoken"
    })
    assert resp.status == 406


async def test_user_info(cli):
    await login(cli)
    resp = await cli.get("/api/v1/user")
    data = await resp.json()
    assert data["name"] == "Test" and data["surname"] == "User" \
        and data["privileges"] == 2 and data["gravatar_hash"] == "28ad76f33b98f31da09ed225587f2f8a"
