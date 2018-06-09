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
            await cur.execute("SELECT id FROM users WHERE email = 'valid@emailaddr.es' LIMIT 1")
            assert await cur.fetchone()


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
