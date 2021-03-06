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

            "REDIS_HOST": config("REDIS_HOST", default="127.0.0.1"),
            "REDIS_PORT": config("REDIS_PORT", default="6379", cast=int),
            "REDIS_DATABASE": config("REDIS_DATABASE", default="0", cast=int),
            "REDIS_TEST_DATABASE": config("REDIS_TEST_DATABASE", default="1", cast=int),
            "REDIS_PASSWORD": config("REDIS_PASSWORD", default=None),
            "REDIS_POOL_SIZE": config("REDIS_POOL_SIZE", default="8", cast=int),

            "DB_HOST": config("DB_HOST"),
            "DB_PORT": config("DB_PORT", default="3306", cast=int),
            "DB_USERNAME": config("DB_USERNAME"),
            "DB_PASSWORD": config("DB_PASSWORD"),
            "DB_NAME": config("DB_NAME", default="fitoemanews"),
            "TEST_DB_NAME": config("TEST_DB_NAME", default="fitoemanewstest"),

            "DB_POOL_MIN_SIZE": config("DB_POOL_MIN_SIZE", default="1", cast=int),
            "DB_POOL_MAX_SIZE": config("DB_POOL_MAX_SIZE", default="8", cast=int),

            "TELEGRAM_TOKEN": config("TELEGRAM_TOKEN", default=None),

            "MAILGUN_DOMAIN": config("MAILGUN_DOMAIN", default=None),
            "MAILGUN_KEY": config("MAILGUN_KEY", default=None),
            "MAILGUN_DEFAULT_SENDER": config("MAILGUN_DEFAULT_SENDER", default=None),

            "DEBUG": config("DEBUG", default="false", cast=bool),
            "WEB_BASE_URL": config("WEB_BASE_URL", default="http://172.16.10.100"),

            "SENTRY_DSN": config("SENTRY_DSN", default=""),
            "RAVEN_QUEUE_SIZE": config("RAVEN_QUEUE_SIZE", default="256", cast=int),
            "RAVEN_WORKERS": config("RAVEN_WORKERS", default="2", cast=int),
        }

    def __getitem__(self, item):
        return self._config[item]
