import time

from singletons.emanews import EmaNews
from tests.conftest import login


async def test_telegram_token_generate(cli):
    await login(cli)
    resp = await cli.get("/api/v1/telegram")
    data = await resp.json()
    assert data["telegram_link"]
    bot_username = (await EmaNews().bot.get_me())["username"]
    assert data["telegram_link"].startswith("https://telegram.me/{}?start=".format(bot_username))
    assert len(data["telegram_link"].split("=")[1]) == 16


async def test_telegram_token_already_generated_returns_same(cli):
    await login(cli)

    resp = await cli.get("/api/v1/telegram")
    data = await resp.json()
    deep_link_token = data["telegram_link"].split("=")[1]
    assert len(deep_link_token) == 16

    resp = await cli.get("/api/v1/telegram")
    data = await resp.json()
    assert deep_link_token in data["telegram_link"]


# async def test_telegram_start_command(cli, telegram_bot, telegram_user_bot):
#     await login(cli)
#
#     resp = await cli.get("/api/v1/telegram")
#     data = await resp.json()
#     deep_link_token = data["telegram_link"].split("=")[1]
#     assert len(deep_link_token) == 16
#
#     bot_username = (await EmaNews().bot.get_me())["username"]
#     telegram_user_bot.send_message(bot_username, "/start {}".format(deep_link_token))
#
#     for message in telegram_user_bot.iter_messages(bot_username, limit=1):
#         assert message.message.startswith("👏 Congratulazioni!")
#
#     async with EmaNews().db.acquire() as conn:
#         async with conn.cursor() as cur:
#             await cur.execute("SELECT telegram_user_id FROM users WHERE id = 1 LIMIT 1")
#             r = await cur.fetchone()
#             assert r["telegram_user_id"] == str(telegram_user_bot.get_me().id)
#             await cur.execute("SELECT * FROM telegram_link_tokens WHERE user_id = 1 LIMIT 1")
#             assert (await cur.fetchone()) is None


# async def test_telegram_token_already_linked(cli):
#     await login(cli)
#     await cli.get("/api/v1/telegram")
#     resp = await cli.get("/api/v1/telegram")
#     assert resp.status == 406
#     async with EmaNews().db.acquire() as conn:
#         async with conn.cursor() as cur:
#             await cur.execute("SELECT * FROM telegram_link_tokens WHERE user_id = 1 LIMIT 1")
#             assert (await cur.fetchone()) is None


async def test_telegram_token_not_authenticated(cli):
    resp = await cli.delete("/api/v1/telegram")
    assert resp.status == 401


async def test_telegram_unlink(cli):
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE users SET telegram_user_id = 1337 WHERE id = 1 LIMIT 1")
            await conn.commit()

    await login(cli)
    resp = await cli.delete("/api/v1/telegram")
    assert resp.status == 200
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT telegram_user_id FROM users WHERE id = 1 LIMIT 1")
            assert (await cur.fetchone())["telegram_user_id"] is None


async def test_telegram_token_expire_timestamp(cli):
    await login(cli)
    resp = await cli.get("/api/v1/telegram")
    assert resp.status == 200
    data = await resp.json()
    # deep_link_token = data["telegram_link"].split("=")[1]
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT `expire` FROM telegram_link_tokens WHERE user_id = 1 LIMIT 1")
            assert (await cur.fetchone())["expire"] > int(time.time())


async def test_telegram_token_new_after_expire(cli):
    await login(cli)
    resp = await cli.get("/api/v1/telegram")
    assert resp.status == 200
    old_data = await resp.json()
    assert "telegram_link" in old_data

    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE telegram_link_tokens SET `expire` = 1 WHERE user_id = 1 LIMIT 1")
            await conn.commit()

    resp = await cli.get("/api/v1/telegram")
    assert resp.status == 200
    new_data = await resp.json()
    assert "telegram_link" in old_data and new_data["telegram_link"] != old_data["telegram_link"]

    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM telegram_link_tokens WHERE token = %s LIMIT 1",
                              (old_data["telegram_link"].split("=")[1],))
            assert (await cur.fetchone()) is None


# async def test_telegram_start_invalid_token(cli, telegram_bot, telegram_user_bot):
#     bot_username = (await EmaNews().bot.get_me())["username"]
#     telegram_user_bot.send_message(bot_username, "/start ihfihfwhi")
#     for message in telegram_user_bot.iter_messages(bot_username, limit=1):
#         assert message.message.startswith("☹️ Si è verificato un errore!")
