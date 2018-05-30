async def test_ping(unit_cli):
    resp = await unit_cli.get("/api/v1/ping")
    assert resp.status == 200
    assert (await resp.json())["message"] == "ok"


async def test_one_int_no_args(unit_cli):
    resp = await unit_cli.get("/api/v1/one_int")
    assert resp.status == 400
    assert (await resp.json())["message"].startswith("Missing keys:")


async def test_one_int_empty(unit_cli):
    assert (await unit_cli.get("/api/v1/one_int?value=")).status == 400


async def test_one_int_valid(unit_cli):
    resp = await unit_cli.get("/api/v1/one_int", params={
        "value": 10
    })
    assert resp.status == 200
    assert (await resp.json())["value"] == 10


async def test_wrong_method(unit_cli):
    assert (await unit_cli.post("/api/v1/one_int")).status == 405


async def test_sum_str_int(unit_cli):
    for cast in (str, int):
        resp = await unit_cli.post("/api/v1/sum", json={
            "a": cast(10),
            "b": cast(5)
        })
        assert resp.status == 200
        assert (await resp.json())["result"] == 15


async def test_sum_null_all_combinations(unit_cli):
    for a, b in [(x, y) for x in (1, None) for y in (2, None) if type(x) is not int or type(y) is not int]:
        assert (await unit_cli.post("/api/v1/sum", json={
            "a": a,
            "b": b
        })).status == 400


async def test_sum_one_null_other_int(unit_cli):
    assert (await unit_cli.post("/api/v1/sum", json={
        "a": None,
        "b": 10
    })).status == 400


async def test_api_errors(unit_cli):
    for code in (404, 500, 403, 409, 406, 201, 401):
        resp = await unit_cli.get("/api/v1/{}".format(code))
        assert resp.status == code
        data = await resp.json()
        assert "status" in data and "message" in data


async def test_asyncio_cancelled_api_error(unit_cli):
    assert (await unit_cli.get("/api/v1/asyncio_cancelled")).status == 400


async def test_unhandled_api_error(unit_cli):
    resp = await unit_cli.get("/api/v1/unhandled_error")
    assert resp.status == 500
    data = await resp.json()
    assert "status" in data and "message" in data
    assert data["message"] == "Internal server error."


async def test_premade_schema(unit_cli):
    resp = await unit_cli.get("/api/v1/premade_schema", params={
        "a": "test"
    })
    assert resp.status == 200
    assert (await resp.json())["result"] == "test"


async def test_wrong_json_data(unit_cli):
    resp = await unit_cli.post("/api/v1/sum", data=b"garbage data")
    assert resp.status == 400
    assert (await resp.json())["message"] == "Invalid JSON data"
