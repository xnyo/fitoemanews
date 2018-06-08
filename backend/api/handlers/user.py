import bcrypt
from aiohttp import web
from aiohttp.web_request import Request
from email_validator import validate_email
from schema import And, Use
from zxcvbn import zxcvbn

import api
from constants.privileges import Privileges
from exceptions.api import ConflictError
from singletons.emanews import EmaNews


@api.base
@api.args({
    "name": And(
        str,
        Use(lambda x: x.strip()),
        lambda x: 2 <= len(x) <= 64,
        error="Il nome deve essere compreso tra 2 e 64 caratteri"
    ),
    "surname": And(
        str,
        Use(lambda x: x.strip()),
        lambda x: 2 <= len(x) <= 64,
        error="Il cognome deve essere compreso tra 2 e 64 caratteri"
    ),
    "email": And(
        str,
        Use(lambda x: x.strip()),
        lambda x: validate_email(x)["email"],
        error="Indirizzo email non valido"
    ),
    "password": And(
        str,
        Use(lambda x: x.strip()),
        lambda x: ((100 * zxcvbn(x)["score"]) / 4) >= 50,
        Use(lambda x: x.encode()),
        error="La password scelta è troppo debole"
    ),
})
async def handle(request: Request, data):
    async with EmaNews().db.acquire() as conn:
        async with conn.cursor() as cur:
            # Controlla se l'indirizzo email è stato già usato
            await cur.execute("SELECT id FROM users WHERE email = %s LIMIT 1", (data["email"],))
            other_user = await cur.fetchone()
            if other_user:
                # Già usato
                raise ConflictError("Esiste già un altro utente registrato con questo indirizzo email.")

            # Ok, hash password con bcrypt
            bcrypted_password = bcrypt.hashpw(data["password"], bcrypt.gensalt())

            # Insert in db
            await cur.execute(
                "INSERT INTO users (name, surname, email, password, privileges) "
                "VALUES (%s, %s, %s, %s, %s)",
                (
                    data["name"],
                    data["surname"],
                    data["email"],
                    bcrypted_password.decode(),
                    int(Privileges.PENDING_ACTIVATION)
                )
            )
            await conn.commit()

    # Ok!
    return web.json_response({
        "message": "ok"
    })
