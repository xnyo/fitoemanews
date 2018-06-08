async def test_zxcvbn_no_input(cli):
    resp = await cli.get("/api/v1/zxcvbn")
    assert resp.status == 400
    data = await resp.json()
    assert data["message"].startswith("Missing keys")


async def test_zxcvbn_empty_input(cli):
    resp = await cli.get("/api/v1/zxcvbn?input=")
    assert resp.status == 400
    data = await resp.json()
    assert data["message"].startswith("Key 'input' error:")     # schema lambda failure


async def test_zxcvbn_strengths(cli):
    passwords = [
        ("password", 0.),
        ("badpassword", 25.),
        ("strongpassw", 50.),
        ("passwor$75$!", 75.),
        ("fwijwefjwefjw", 100.)
    ]
    for password, strength in passwords:
        resp = await cli.get("/api/v1/zxcvbn", params={
            "input": password
        })
        assert resp.status == 200
        data = await resp.json()
        assert data["strength"] == strength
