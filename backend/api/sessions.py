import json
import logging
from typing import Optional, Any, Dict

from schema import Schema, And, Use, SchemaError

from singletons.emanews import EmaNews
from utils import general


class SessionError(Exception):
    """
    Classe che rappresenta un errore relativo alla sessione
    """
    pass


class Session:
    """
    Sessione web
    """
    # Secondi prima dello scadere della sessione
    SESSION_EXPIRE_TIME = 86400

    # Schema dei dati memorizzati in redis
    STORE_SCHEMA = Schema(
        And(
            Use(json.loads),
            {
                "user_id": int,
                "data": dict
            }
        ),
    )
    logger = logging.getLogger("session")

    def __init__(self, user_id: int, token: Optional[str]=None, data: Optional[Dict[str, Any]]=None):
        """
        Inizializza un nuovo oggetto sessione.
        Questa classe non andrebbe istanzata manualmente.
        Utilizzare `SessionFactory` per creare o caricare le sessioni.

        :param user_id: id utente. Obbligatorio.
        :type user_id: int
        :param token: token della sessione.
        :type token: Optional[str]
        :param data: dati della sessione.
        :type data: Optional[Dict[str, Any]]
        """
        self.user_id: int = user_id
        self.token: Optional[str] = token
        self.session_data: Dict[str, Any] = data if data is not None else {}

    async def destroy(self):
        """
        Distrugge la sessione attuale da redis.

        :return:
        """
        await SessionFactory.delete_from_redis(self.token)

    async def generate_valid_token(self):
        """
        Genera ed imposta un valore valido (non usato) a `self.token`.

        :return:
        """
        s = True
        while s:
            t = general.random_string_secure(64)
            s = await EmaNews().redis.get("emanews:session:{}".format(t))
        self.token = t

    @property
    def store_data(self) -> Dict[str, Any]:
        """
        Ritorna i ati da memorizzare in redis.

        :return: dati da memorizzare in redis
        :rtype: Dict[str, Any]
        """
        return {
            "user_id": self.user_id,
            "data": self.session_data
        }

    async def store(self):
        """
        Salva questa sessione in redis

        :return:
        """
        self.logger.debug("Saving session {} for user {}".format(self.token, self.user_id))
        await EmaNews().redis.set(
            "emanews:session:{}".format(self.token),
            json.dumps(self.store_data),
            expire=Session.SESSION_EXPIRE_TIME
        )


class SessionFactory:
    logger = logging.getLogger("session.factory")

    @classmethod
    async def load_from_redis(cls, token: str) -> Session:
        """
        Carica una sessione da redis.

        :param token: Token della sessione da caricare
        :type token: str
        :return: Oggetto sessione corrispondente
        :rtype: Session
        :raises: SessionError
        """
        cls.logger.debug("Loading session with key {} from redis".format(token))
        session_data = await EmaNews().redis.get("emanews:session:{}".format(token))
        if not session_data:
            raise SessionError("Invalid session token")
        try:
            session_data = Session.STORE_SCHEMA.validate(session_data.decode())
        except SchemaError as e:
            raise SessionError("Invalid store schema: {}".format(e))
        return Session(
            token=token,
            user_id=session_data["user_id"],
            data=session_data["data"]
        )

    @classmethod
    async def new_session(cls, user_id: int, data: Optional[Dict[str, Any]]=None) -> Session:
        """
        Crea una nuova sessione per un utente, con token casuale e la salva in redis.
        
        :param user_id: id utente
        :type user_id: int
        :param data: dati aggiuntivi della sessione da salvare in redis.
        :type data: Optional[Dict[str, Any]]
        :return: oggetto sessione
        :rtype: Session
        """
        s = Session(user_id, data=data)
        await s.generate_valid_token()
        await s.store()
        return s

    @classmethod
    async def delete_from_redis(cls, token: str):
        """
        Elimina una sessione da redis.

        :param token: token della sessione da eliminare
        :return:
        """
        cls.logger.debug("Destroying session with key {} from redis".format(token))
        await EmaNews().redis.delete("emanews:session:{}".format(token))
