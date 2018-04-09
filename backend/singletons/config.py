from decouple import config

from utils.singletons import singleton


@singleton
class Config:
    def __init__(self):
        self._config = {
            "DB_HOST": config("DB_HOST"),
            "DB_USERNAME": config("DB_USERNAME"),
            "DB_PASSWORD": config("DB_PASSWORD"),
            "DB_NAME": config("DB_NAME"),

            "DB_POOL_MIN_SIZE": config("DB_POOL_MIN_SIZE", default="1", cast=int),
            "DB_POOL_MAX_SIZE": config("DB_POOL_MAX_SIZE", default="8", cast=int),
        }

    def __getitem__(self, item):
        return self._config[item]
