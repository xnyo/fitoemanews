import logging
from typing import Optional

from constants.notifications import NotificationWhen, NOTIFICATORS
from singletons.emanews import EmaNews


async def notify(event: NotificationWhen, fmt: Optional[dict], herb_id: Optional[int]=None):
    """
    Invia una notifica a tutti gli utenti che hanno attivato
    le notifiche per l'evento specificato.

    :param event: evento per cui mandare la notifica
    :param fmt: dizionaro con dati aggiuntivi con cui formattare il testo del messaggio
                 (e la tastiera, nel caso di Telegram)
    :param herb_id: id erba di questa notifica. Usato per inviare la notifica agli utenti
                     che desiderano ricevere le notifiche per alcune erbe.
                     Se `None`, invia la notifica a tutti.
    :return:
    """
    if EmaNews().no_notifications:
        logging.getLogger("notifications").warning("Missed notification {} {} [{}]".format(event, fmt, herb_id))
        return

    if event not in NOTIFICATORS:
        raise KeyError("There's no notificator for event `{}`".format(event))

    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            if herb_id is None:
                # Generale, senza filtro erbe
                q = "SELECT id, notify_by, email, telegram_user_id FROM users " \
                    "WHERE notify_when & %s > 0 AND notify_by > 0"
                p = (int(event),)
            else:
                # Con filtro erbe
                q = "SELECT users.id, notify_by, email, telegram_user_id FROM users " \
                    "LEFT JOIN notify_herbs ON users.id = notify_herbs.user_id " \
                    "WHERE notify_when & %s > 0 AND notify_by > 0 AND " \
                    "(notify_herbs.herb_id = %s OR users.notify_all = 1)"
                p = (int(event), herb_id)
            await cur.execute(q, p)
            users = await cur.fetchall()
            for user in users:
                for by, notification in NOTIFICATORS[event].items():
                    if user["notify_by"] & by > 0:
                        await notification.send(user, fmt)
