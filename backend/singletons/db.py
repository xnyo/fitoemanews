import aiomysql

from utils.singletons import singleton


@singleton
class Db:
    def __init__(self):
        self._pool = None

    @classmethod
    async def create(cls, *args, **kwargs):
        self = Db()
        self.config = {**kwargs}
        self._pool = await aiomysql.create_pool(*args, **kwargs)
        return self

    def __getattr__(self, item):
        if self._pool is not None:
            return self._pool.__getattribute__(item)

