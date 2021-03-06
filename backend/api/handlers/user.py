import bcrypt
from aiohttp import web
from aiohttp.web_request import Request
from email_validator import validate_email
from schema import And, Use
from zxcvbn import zxcvbn

import api
from api.schema import StrippedString, Password
from api.sessions import Session
from constants.privileges import Privileges
from exceptions.api import ConflictError
from singletons.config import Config
from singletons.emanews import EmaNews
from utils import general, gravatar


@api.base
@api.guest_only
@api.args({
    "name": And(
        StrippedString,
        lambda x: 2 <= len(x) <= 64,
        error="Il nome deve essere compreso tra 2 e 64 caratteri"
    ),
    "surname": And(
        StrippedString,
        lambda x: 2 <= len(x) <= 64,
        error="Il cognome deve essere compreso tra 2 e 64 caratteri"
    ),
    "email": And(
        StrippedString,
        lambda x: validate_email(x)["email"],
        error="Indirizzo email non valido"
    ),
    "password": Password,
})
async def post(request: Request, *, params):
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            # Controlla se l'indirizzo email è stato già usato
            await cur.execute("SELECT id FROM users WHERE email = %s LIMIT 1", (params["email"],))
            other_user = await cur.fetchone()
            if other_user:
                # Già usato
                raise ConflictError("Esiste già un altro utente registrato con questo indirizzo email.")

            # Ok, hash password con bcrypt
            bcrypted_password = bcrypt.hashpw(params["password"], bcrypt.gensalt())

            # Insert in db
            await cur.execute(
                "INSERT INTO users (name, surname, email, password, privileges) "
                "VALUES (%s, %s, %s, %s, %s)",
                (
                    params["name"],
                    params["surname"],
                    params["email"],
                    bcrypted_password.decode(),
                    int(Privileges.PENDING_ACTIVATION)
                )
            )

            # Genera e salva token attivazione account
            token = general.random_string_secure(64)
            await cur.execute("INSERT INTO activation_tokens (user_id, token) VALUES (%s, %s)",
                              (cur.lastrowid, token))
            await conn.commit()

            # Invio email
            await EmaNews().mailgun_client.send(
                to=params["email"],
                subject="Conferma il tuo account EmaNews",
                html="Clicca sul seguente link per attivare il tuo account EmaNews: "
                     "<a href='{}/activate/{}'>Attiva account</a>".format(
                    Config()["WEB_BASE_URL"].rstrip("/"), token
                )
            )

    # Ok!
    return web.json_response({
        "message": "ok"
    })


@api.base
@api.protected()
async def get(request: Request, *, session: Session):
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT id, name, surname, privileges, email FROM users WHERE id = %s LIMIT 1", (session.user_id,)
            )
            db_user = await cur.fetchone()
    db_user["gravatar_hash"] = gravatar.get_hash(db_user["email"])
    del db_user["email"]
    return web.json_response(db_user)
