import inspect
import logging
import traceback

from raven import Client

from singletons.emanews import EmaNews


def on_exception():
    """
    Logga l'ultima `Exception` su Sentry tramite il client raven,
    se abilitato

    :return:
    """
    logging.getLogger().error(traceback.format_exc())
    if EmaNews().is_raven_enabled:
        EmaNews().raven.captureException()
    else:
        logging.getLogger("raven_client").warning("Raven client disabled, exception not tracked.")


def capture(func):
    """
    Decora una coroutine per loggare tutte le `Exception` su Sentry, se abilitato

    :param func:
    :return:
    """

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception:
            on_exception()

    return wrapper


def capture_sync(func):
    """
    Decora una funzione per loggare tutte le `Exception` su Sentry, se abilitato

    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            on_exception()

    return wrapper


class CaptureClass(type):
    """
    Metaclasse che decora tutti i metodi e coroutine con
    `capture_sync` o `capture_async` per loggare tutte le
    `Exception` a sentry, se abilitato
    """
    def __new__(mcs, name, bases, namespace):
        # Il controllo se raven è abilitato # o meno avviene
        # dentro on_exception perchè se una classe
        # viene importata prima di inizializzare EmaNews
        # (come avviene nel 99% dei nei module-level imports)
        # allora non avrà il decorator
        for attr in namespace:
            value = namespace[attr]
            if callable(value):
                if inspect.iscoroutinefunction(value):
                    # Coroutine
                    namespace[attr] = capture(value)
                else:
                    # Metodo
                    capture_sync(value)
        return type.__new__(mcs, name, bases, namespace)
