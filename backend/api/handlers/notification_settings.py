import logging

from aiohttp import web
from aiohttp.web_request import Request
from schema import And, Or, Optional

import api
from api.sessions import Session
from constants.notifications import NotificationWhen, NotificationBy
from singletons.emanews import EmaNews


@api.base
@api.protected()
async def get(request: Request, *, session: Session):
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT notify_when, notify_by, notify_all, telegram_user_id "
                              "FROM users WHERE id = %s LIMIT 1", (session.user_id,))
            notification_settings = await cur.fetchone()
            if not notification_settings["notify_all"]:
                await cur.execute("SELECT herbs.id, herbs.latin_name, herbs.english_name, herbs.botanic_name "
                                  "FROM notify_herbs JOIN herbs ON notify_herbs.herb_id = herbs.id "
                                  "WHERE user_id = %s", (session.user_id,))
                herbs = await cur.fetchall()
            else:
                herbs = True

    return web.json_response({
        "when": [
            x.name for x in [
                NotificationWhen(notification_settings["notify_when"]) & y
                for y in NotificationWhen
            ] if x != NotificationWhen.NONE
        ],
        "by": [
            x.name for x in [
                NotificationBy(notification_settings["notify_by"]) & y
                for y in NotificationBy if y != NotificationBy.NONE
            ] if x != NotificationWhen.NONE
        ],
        "telegram_linked": notification_settings["telegram_user_id"] is not None,
        "herbs": herbs
    })


@api.base
@api.protected()
@api.args({
    "when": Optional(And(list, [x.name for x in NotificationWhen], error="Parametro when non valido")),
    "by": Optional(And(list, [x.name for x in NotificationBy], error="Parametro by non valido")),
    "herbs": Optional(Or(
        True,
        And(
            list, lambda x: all([type(y) is int for y in x])
        ), error="notify_herbs deve essere una lista di interi oppure True"
    ))
})
async def post(request: Request, *, params, session: Session):
    updates = ", ".join(
        ["notify_{name} = %({name})s".format(name=k) for k in ("when", "by") if k in params] +
        ["notify_all = %(notify_all)s"] if "herbs" in params else []
    )

    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            q = "UPDATE users SET {} WHERE id = %(user_id)s LIMIT 1".format(updates)
            p = {
                        "when": sum([NotificationWhen[k] for k in params["when"]]),
                        "by": sum([NotificationBy[k] for k in params["by"]]),
                        "user_id": session.user_id,
                        "notify_all": "herbs" in params and type(params["herbs"]) is bool
                }
            logging.debug(q)
            logging.debug(p)
            await cur.execute(
                q,
                p
            )
            if "herbs" in params:
                await cur.execute("DELETE FROM notify_herbs WHERE user_id = %s", (session.user_id,))
                if type(params["herbs"]) is list:
                    for herb_id in params["herbs"]:
                        await cur.execute(
                            "INSERT IGNORE INTO notify_herbs (user_id, herb_id) VALUES (%s, %s)",
                            (session.user_id, herb_id)
                        )
            await conn.commit()
    return web.json_response({
        "message": "ok"
    })
