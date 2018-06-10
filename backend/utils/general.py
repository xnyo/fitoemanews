import string

import hashlib
import random


def random_string_secure(l: int) -> str:
    """
    Genera una stringa casuale di `l` caratteri

    :param l: lunghezza della stringa
    :return: stringa casuale
    """
    return "".join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(l))


def md5(s: str) -> str:
    """
    Ritorna l'hash md5 di una stringa

    :param s: stringa
    :return: hash md5 di `s`
    """
    m = hashlib.md5()
    m.update(s.encode())
    return m.hexdigest()
