from utils import general


def get_hash(email: str):
    """
    Ritorna l'hash di un indirizzo email, da usare con gravatar
    (http://en.gravatar.com/site/implement/hash/)

    :param email: indirizzo email
    :return: hash da usare con gravatar
    """
    return general.md5(email.strip().lower())
