from constants.privileges import Privileges
from singletons.emanews import EmaNews


async def test_sign_up_valid(cli):
    resp = await cli.post("/api/v1/user", json={
        "name": "Name",
        "surname": "Surname",
        "email": "valid@emailaddr.es",
        "password": "somequalitypassword"
    })
    assert resp.status == 200
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT users.id AS uid, activation_tokens.id AS aid, privileges "
                              "FROM users JOIN activation_tokens "
                              "ON users.id = activation_tokens.user_id "
                              "WHERE email = 'valid@emailaddr.es' LIMIT 1")
            row = await cur.fetchone()
            assert row and row["uid"] and row["aid"]
            assert row["privileges"] == Privileges.PENDING_ACTIVATION


async def test_sign_up_missing_all_fields(cli):
    resp = await cli.post("/api/v1/user")
    assert resp.status == 400


async def test_sign_up_missing_some_fields(cli):
    fields = ["name", "surname", "email", "password"]
    for field in fields:
        resp = await cli.post("/api/v1/user", json={
            field: "gibberish"
        })
        assert resp.status == 400


async def test_sign_up_all_fields_empty_strings(cli):
    fields = ["name", "surname", "email", "password"]
    for field in fields:
        resp = await cli.post("/api/v1/user", json={
            field: ""
        })
        assert resp.status == 400


async def test_sign_up_name_too_short(cli):
    resp = await cli.post("/api/v1/user", json={
        "name": "o",
        "surname": "Surname",
        "email": "valid@emailaddr.es",
        "password": "somequalitypassword"
    })
    assert resp.status == 400
    data = await resp.json()
    assert data["message"].startswith("Il nome deve essere compreso")


async def test_sign_up_surname_too_short(cli):
    resp = await cli.post("/api/v1/user", json={
        "name": "Name",
        "surname": "o",
        "email": "valid@emailaddr.es",
        "password": "somequalitypassword"
    })
    assert resp.status == 400
    data = await resp.json()
    assert data["message"].startswith("Il cognome deve essere compreso")


async def test_sign_up_invalid_email(cli):
    resp = await cli.post("/api/v1/user", json={
        "name": "Name",
        "surname": "Surname",
        "email": "not an email",
        "password": "somequalitypassword"
    })
    assert resp.status == 400
    data = await resp.json()
    assert data["message"] == "Indirizzo email non valido"


async def test_sign_up_password_strength(cli):
    resp = await cli.post("/api/v1/user", json={
        "name": "Name",
        "surname": "Surname",
        "email": "real@emailaddr.es",
        "password": "password"
    })
    assert resp.status == 400
    data = await resp.json()
    assert data["message"] == "La password scelta è troppo debole"


async def test_sign_up(cli):
    resp = await cli.post("/api/v1/user", json={
        "name": "Name",
        "surname": "Surname",
        "email": "not an email",
        "password": "somequalitypassword"
    })
    assert resp.status == 400
    data = await resp.json()
    assert data["message"] == "Indirizzo email non valido"


async def test_activate_no_token(cli):
    resp = await cli.post("/api/v1/activate/")
    assert resp.status == 404


async def test_activate_invalid_token(cli):
    resp = await cli.post("/api/v1/activate/asdiohasdihjsad")
    assert resp.status == 404
    data = await resp.json()
    assert data["message"] == "Token di attivazione non valido"


async def test_activate_invalid_token(cli):
    resp = await cli.post("/api/v1/activate/asdiohasdihjsad")
    assert resp.status == 404
    data = await resp.json()
    assert data["message"] == "Token di attivazione non valido"


async def test_activate_valid_token(cli):
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT token, user_id FROM activation_tokens LIMIT 1")
            token = await cur.fetchone()
            assert token and "token" in token

        resp = await cli.post("/api/v1/activate/{}".format(token["token"]))
        assert resp.status == 200
        data = await resp.json()
        assert data["message"] == "ok"

    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT token FROM activation_tokens LIMIT 1")
            assert not await cur.fetchone()

            await cur.execute("SELECT privileges FROM users WHERE id = %s LIMIT 1", (token["user_id"],))
            privileges = await cur.fetchone()
            assert privileges and privileges["privileges"] & Privileges.NORMAL
