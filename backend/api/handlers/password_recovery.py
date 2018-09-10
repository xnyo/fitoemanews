import logging

from aiohttp import web
from aiohttp.web_request import Request

import api
from singletons.config import Config
from singletons.emanews import EmaNews
from utils import general


@api.base
@api.guest_only
@api.args({"email": str})
async def handle(request: Request, *, params):
    ok_response = web.json_response({
        "message": "ok"
    })
    logging.debug("Requested password reset for {}".format(params["email"]))

    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM users WHERE email = %s AND privileges & 2 > 0 LIMIT 1", (params["email"],))
            db_user = await cur.fetchone()
            if not db_user:
                logging.debug("Failed silently")
                return ok_response

            # Cancella token scaduti per questo utente
            await cur.execute(
                "DELETE FROM password_reset_tokens WHERE `expire` <= UNIX_TIMESTAMP() AND user_id = %s",
                (db_user["id"])
            )

            # Recupera eventuale token esistente
            await cur.execute(
                "SELECT token FROM password_reset_tokens WHERE user_id = %s AND `expire` > UNIX_TIMESTAMP() LIMIT 1",
                (db_user["id"],)
            )
            db_token = await cur.fetchone()
            if not db_token:
                # Nessun token, generane uno
                logging.debug("Generating new token")
                token = general.random_string_secure(64)
                await cur.execute(
                    "INSERT INTO password_reset_tokens (user_id, token, `expire`) "
                    "VALUES (%s, %s, UNIX_TIMESTAMP() + 3600)",
                    (db_user["id"], token)
                )
                await conn.commit()
            else:
                # Token esistente
                logging.debug("Using pre-existing token")
                token = db_token["token"]

            # Invia email
            await EmaNews().mailgun_client.send(
                to=params["email"],
                subject="Recupero password EmaNews",
                html="Clicca sul seguente link per reimpostare la tua password del tuo account EmaNews: "
                     "<a href='{}/password_reset/{}'>Reimposta password</a>.<br>"
                     "Il link scade tra 60 minuti. Se non sei stato tu a richiedere il reset "
                     "della tua password, ignora questa email.".format(
                    Config()["WEB_BASE_URL"].rstrip("/"), token
                )
            )
    return ok_response
