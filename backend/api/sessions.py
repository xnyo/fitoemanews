import json
import logging
from typing import Optional

from schema import Schema, And, Use, SchemaError

from singletons.emanews import EmaNews
from utils import general


class SessionError(Exception):
    pass


class Session:
    SESSION_EXPIRE_TIME = 86400
    STORE_SCHEMA = Schema(
        And(
            Use(json.loads),
            {"user_id": str}
        ),
    )
    logger = logging.getLogger("session")

    def __init__(self, user_id: int, token: str=None):
        self.user_id: int = user_id
        self.token: Optional[str] = token

    @classmethod
    async def load_from_redis(cls, token: str) -> "Session":
        cls.logger.debug("Loading session with key {} from redis".format(token))
        session_data = await EmaNews().redis.get("emanews:sessions:{}".format(token))
        if not session_data:
            raise SessionError("Invalid session token")
        try:
            session_data = Session.STORE_SCHEMA.validate(session_data.decode())
        except SchemaError:
            raise SessionError("Invalid store schema")
        return Session(user_id=session_data["user_id"], token=session_data["token"])

    async def generate_valid_token(self):
        s = True
        while s:
            t = general.random_string_secure(64)
            s = await EmaNews().redis.get("emanews:session:{}".format(t))
        self.token = t

    @classmethod
    async def new_session(cls, user_id: int) -> "Session":
        s = Session(user_id)
        await s.generate_valid_token()
        await s.store()
        return s

    @property
    def store_data(self):
        return {
            "user_id": self.user_id
        }

    async def store(self):
        self.logger.debug("Saving session {} for user {}".format(self.token, self.user_id))
        await EmaNews().redis.set(
            "emanews:session:{}".format(self.token),
            json.dumps(self.store_data),
            expire=Session.SESSION_EXPIRE_TIME
        )
