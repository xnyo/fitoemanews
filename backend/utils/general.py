import string

import random


def random_string_secure(l: int) -> str:
    """
    Genera una stringa casuale di `l` caratteri

    :param l: lunghezza della stringa
    :return: stringa casuale
    """
    return "".join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(l))
