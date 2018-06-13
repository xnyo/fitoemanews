from aiohttp import web
from aiohttp.web_request import Request

import api
from api.sessions import Session
from constants.notifications import NotificationEvents, NotificationBy
from singletons.emanews import EmaNews


@api.base
@api.protected()
async def handle(request: Request, *, session: Session):
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT notify_what, notify_by, notify_all, telegram_user_id "
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
                NotificationEvents(notification_settings["notify_what"]) & y
                for y in NotificationEvents
            ] if x != NotificationEvents.NONE
        ],
        "by": [
            x.name for x in [
                NotificationBy(notification_settings["notify_by"]) & y
                for y in NotificationBy if y != NotificationBy.NONE
            ] if x != NotificationEvents.NONE
        ],
        "telegram_linked": notification_settings["telegram_user_id"] is not None,
        "notify_herbs": herbs
    })
