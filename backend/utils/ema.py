import time
from collections import namedtuple
from datetime import datetime
from typing import Union, Optional

# EmaDocument = namedtuple("EmaDocument", ["name", "type", "url", "language", "first_published", "last_updated_ema"])
# EmaDocument.__new__.__defaults__ = (None,) * len(EmaDocument._fields)
EmaHerb = namedtuple("EmaHerb", ["latin_name", "botanic_name", "english_name", "status", "url", "last_updated_ema"])


def ema_date_to_unix(d: Union[str, int]) -> Optional[int]:
    if type(d) is str:
        if not d:
            return None
        return int(time.mktime(
            datetime.strptime(d, "%Y-%m-%d").timetuple()
        ))
    else:
        return d


class EmaDocument:
    def __init__(
        self, name: str, _type: str, url: str, language: str,
        first_published: Union[str, int], last_updated_ema: Union[str, int]
    ):
        self.name = name
        self.type = _type
        self.url = url
        self.language = language
        self.first_published = ema_date_to_unix(first_published)
        self.last_updated_ema = ema_date_to_unix(last_updated_ema)

    def __repr__(self):
        return "EmaDocument<{}>".format(self.name)
