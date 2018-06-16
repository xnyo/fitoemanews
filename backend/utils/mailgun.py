import logging
from typing import Optional

import aiohttp


class MailgunError(Exception):
    """
    Classe che rappresenta un errore di mailgun
    """
    pass


class MailgunClient:
    """
    Client mailgun asincrono
    """
    logger = logging.getLogger("mailgun")

    def __init__(self, domain: str, key: str, default_from: Optional[str]=None):
        """
        Inizializza un nuovo client mailgun

        :param domain: dominio
        :param key: api key mailgun
        :param default_from: mittente di default (es: `noreply@example.com`)
        """
        self.domain: str = domain
        self.key: str = key
        self.default_from: Optional[str] = default_from

    async def send(self, to: str, subject: str, text: str=None, html: str=None, _from: str=None):
        """
        Invia una mail con mailgun

        :param to: Email destinatario
        :param subject: Oggetto email
        :param text: Contenuto testuale della mail. opzionale.
        :param html: Contenuto html della mail. opzionale.
        :param _from: Indirizzo mittente. opzionale. l'indirizzo di default è `self.default_from`.
        :raise: MailgunError
        :return:
        """
        self.logger.debug("""Sending email with mailgun to {} ({})
        {}""".format(to, subject, text if text is not None else html))
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.mailgun.net/v3/{}/messages".format(self.domain), data={
                "from": self.default_from if _from is None else _from,
                "to": to,
                "subject": subject,
                "text": text,
                "html": html
            }, auth=aiohttp.BasicAuth("api", self.key)) as resp:
                if resp.status != 200:
                    raise MailgunError(resp)


class DummyMailgunClient(MailgunClient):
    """
    Client mailgun fittizio
    """
    def __init__(self, *args, **kwargs):
        """
        Visualizza un messaggio di warning anzichè inizializzare il client mailgun.

        :param args:
        :param kwargs:
        """
        self.logger.warning("Mailgun is disabled.")

    async def send(self, *args, **kwargs):
        """
        Visualizza un messaggio di warning anzichè inviare la mail.

        :param args:
        :param kwargs:
        :return:
        """
        self.logger.warning("Attempted to send an email, but mailgun is disabled.")
