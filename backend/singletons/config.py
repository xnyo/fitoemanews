from decouple import config

from utils.singletons import singleton


@singleton
class Config:
    """
    Singleton file configurazione.
    È possibile accedere ai valori del file di configurazione con la sintassi di un dict
    ```
    >>> print(Config()["DB_NAME"])
    fitoemanews
    ```
    """
    def __init__(self):
        self._config = {
            "HTTP_HOST": config("HTTP_HOST", default="127.0.0.1"),
            "HTTP_PORT": config("HTTP_PORT", default="8000", cast=int),

            "DB_HOST": config("DB_HOST"),
            "DB_PORT": config("DB_PORT", default="3306", cast=int),
            "DB_USERNAME": config("DB_USERNAME"),
            "DB_PASSWORD": config("DB_PASSWORD"),
            "DB_NAME": config("DB_NAME", default="fitoemanews"),
            "TEST_DB_NAME": config("TEST_DB_NAME", default="fitoemanewstest"),

            "DB_POOL_MIN_SIZE": config("DB_POOL_MIN_SIZE", default="1", cast=int),
            "DB_POOL_MAX_SIZE": config("DB_POOL_MAX_SIZE", default="8", cast=int),

            "DEBUG": config("DEBUG", default="false", cast=bool),
        }

    def __getitem__(self, item):
        return self._config[item]
