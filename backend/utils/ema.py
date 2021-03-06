import time
from collections import namedtuple
from datetime import datetime
from typing import Union, Optional

EmaHerb = namedtuple("EmaHerb", ["latin_name", "botanic_name", "english_name", "status", "url", "last_updated_ema"])


def ema_date_to_unix(d: str) -> Optional[int]:
    """
    Converte una data dal formato usato dall'EMA in una UNIX timestamp

    :param d: data formato ema
    :return: unix timewstamp (int) o `None` se la data non è presente
    """
    if not d:
        return None
    return int(time.mktime(
        datetime.strptime(d, "%Y-%m-%d").timetuple()
    ))


class EmaDocument:
    """
    Documento EMA
    """
    def __init__(
        self, name: str, _type: str, url: str, language: str,
        first_published: Union[str, int], last_updated_ema: Union[str, int]
    ):
        """
        Inizializza un nuovo documento

        :param name: nome documento
        :param _type: tipo documento
        :param url: URL documento
        :param language: lingua documento
        :param first_published: data pubblicazione, nel formato dell'ema o unix
        :param last_updated_ema: data aggiornamento, nel formato dell'ema o unix
        """
        self.name = name
        self.type = _type
        self.url = url
        self.language = language
        self.first_published = ema_date_to_unix(first_published) if type(first_published) is str else first_published
        self.last_updated_ema = ema_date_to_unix(last_updated_ema) if type(last_updated_ema) is str else last_updated_ema

    def __repr__(self):
        return "EmaDocument<{}>".format(self.name)
