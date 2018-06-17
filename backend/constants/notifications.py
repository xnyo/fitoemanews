import json

from abc import abstractmethod, ABC
from enum import IntFlag, auto
from typing import List, Dict, Optional

from singletons.emanews import EmaNews

TelegramKeyboard = List[List[Dict[str, str]]]


class NotificationWhen(IntFlag):
    """
    Enum che rappresenta gli eventi per
    cui è possibile ricevere notifiche
    """
    NONE = 0
    NEW_MEDICINE = auto()
    MEDICINE_UPDATE = auto()
    NEW_DOCUMENT = auto()
    DOCUMENT_UPDATE = auto()


class NotificationBy(IntFlag):
    """
    Enum che rappresenta come è
    possibile ricevere le notifiche
    """
    NONE = 0
    EMAIL = auto()
    TELEGRAM = auto()


class INotification(ABC):
    """
    Interfaccia notifiche
    """
    FLAG = NotificationBy.NONE

    @abstractmethod
    async def send(self, *args, **kwargs):
        """
        Invia la notifica. Metodo astratto.

        :param args:
        :param kwargs:
        :return:
        """
        pass


class EmailNotification(INotification):
    """
    Notifica via email
    """
    FLAG = NotificationBy.EMAIL

    def __init__(self, subject: str, html: str):
        """
        Inizializza una nuova notifica via email

        :param subject: oggetto email
        :param html: contenuto html della email
        """
        self.subject: str = subject
        self.html: str = html

    async def send(self, user: dict, fmt: Optional[dict]):
        """
        Invia la email all'indirizzo specificato, formattando
        l'oggetto e il contenuto con il dizionario fornito in `fmt`.

        :param user: dizionario con i dati dell'utente, recuperato dal db
        :param fmt: dizionario con cui formattare l'oggetto e il contenuto della email
        :return:
        """
        if "email" not in user:
            raise AttributeError("`email` key not found in `user` dict")
        fmt = {} if fmt is None else fmt
        await EmaNews().mailgun_client.send(
            to=user["email"].format(**fmt),
            subject=self.subject,
            html=self.html.format(**fmt)
        )


class TelegramNotification(INotification):
    """
    Notifica via telegram
    """
    FLAG = NotificationBy.TELEGRAM

    def __init__(self, text, keyboard: Optional[TelegramKeyboard]):
        """
        Inizializza una nuova notifica via telegram.

        :param text: testo del messaggio, in HTML
        :param keyboard: inline keyboard
        """
        self.text: str = text
        self.keyboard: Optional[TelegramKeyboard] = keyboard

    async def send(self, user: dict, fmt: Optional[dict]):
        """
        Invia la notifica via telegram all'utente specificato formattando il
        messaggio e la tastiera con il dizionario passato in `fmt`

        :param user: dizionario con i dati dell'utente, recuperato dal db
        :param fmt: dizionario con cui formattare il messaggio e la tastiera
        :return:
        """
        if "telegram_user_id" not in user:
            raise AttributeError("`telegram_user_id` key not found in `user` dict")
        fmt = {} if fmt is None else fmt
        await EmaNews().bot.send_message(
            chat_id=user["telegram_user_id"],
            text=self.text.format(**fmt),
            parse_mode="html",
            reply_markup=json.dumps(
                {"inline_keyboard": TelegramNotification.format_keyboard(self.keyboard, fmt=fmt)}
            )
        )

    @classmethod
    def format_keyboard(cls, keyboard: TelegramKeyboard, fmt: dict):
        """
        Formatta una tastiera. I valori dei dizionari contenuti nella
        tastiera verranno formattati con il dizionario passato nel parametro `fmt`

        :param keyboard: tastiera
        :param fmt: dizionario per formattare la tastiera
        :return: tastiera formattata
        """
        return [[{k: v.format(**fmt) for k, v in y.items()} for y in x] for x in keyboard]


NOTIFICATORS = {
    NotificationWhen.NEW_MEDICINE: {
        NotificationBy.EMAIL: EmailNotification(
            subject="EmaNews: Nuovo medicinale",
            html="<h4>Un nuovo medicinale è stato inserito. Ecco alcune informazioni:</h4>"
                 "<ul>"
                 "<li><b>Nome latino:</b> {latin_name}</li>"
                 "<li><b>Nome botanico:</b> {botanic_name}</li>"
                 "<li><b>Nome inglese:</b> {english_name}</li>"
                 "<li><b>Stato:</b> {status}</li>"
                 "<li><b>URL EMA:</b> {url}</li>"
                 "</ul>"
                 "<i>Puoi consultare la lista completa delle erbe e dei relativi "
                 "documenti sul sito di EmaNews.</i>"
        ),
        NotificationBy.TELEGRAM: TelegramNotification(
            text="💊 <b>Un nuovo medicinale è stato inserito.</b>\n"
                 "🔸 <b>Nome latino:</b> {latin_name}\n"
                 "🔸 <b>Nome botanico:</b> {botanic_name}\n"
                 "🔸 <b>Nome inglese:</b> {english_name}\n"
                 "🔸 <b>Stato:</b> <code>{status}</code>\n"
                 "\n<i>Puoi consultare la lista completa delle erbe e dei relativi "
                 "documenti sul sito di EmaNews.</i>",
            keyboard=[[{"text": "🔗 Consulta", "url": "{url}"}]]
        )
    },
    NotificationWhen.NEW_DOCUMENT: {
        NotificationBy.EMAIL: EmailNotification(
            subject="EmaNews: Nuovo documento",
            html="<h4>Un nuovo documento è stato inserito. Ecco alcune informazioni:</h4>"
                 "<ul>"
                 "<li><b>Nome:</b> {name}</li>"
                 "<li><b>Tipo:</b> {type}</li>"
                 "<li><b>Erba:</b> {latin_name} ~ {botanic_name} ~ {english_name}</li>"
                 "<li><b>URL:</b> {url}</li>"
                 "</ul>"
                 "<i>Puoi consultare la lista completa delle erbe e dei relativi "
                 "documenti sul sito di EmaNews.</i>"
        ),
        NotificationBy.TELEGRAM: TelegramNotification(
            text="📄 <b>Un nuovo documento è stato inserito.</b>\n"
                 "🔸 <b>Nome:</b> {name}\n"
                 "🔸 <b>Tipo:</b> {type}\n"
                 "🔸 <b>Erba:</b> {latin_name} ~ {botanic_name} ~ {english_name}\n"
                 "\n<i>Puoi consultare la lista completa delle erbe e dei relativi "
                 "documenti sul sito di EmaNews.</i>",
            keyboard=[[{"text": "🔗 Consulta", "url": "{url}"}]]
        )
    },
    NotificationWhen.MEDICINE_UPDATE: {
        NotificationBy.EMAIL: EmailNotification(
            subject="EmaNews: Stato medicinale cambiato",
            html="<h4>Lo stato di un medicinale è cambiato. Ecco le informazioni aggiornate:</h4>"
                 "<ul>"
                 "<li><b>Nome latino:</b> {latin_name}</li>"
                 "<li><b>Nome botanico:</b> {botanic_name}</li>"
                 "<li><b>Nome inglese:</b> {english_name}</li>"
                 "<li><b>Nuovo stato:</b> {status}</li>"
                 "<li><b>URL EMA:</b> {url}</li>"
                 "</ul>"
                 "<i>Puoi consultare la lista completa delle erbe e dei relativi "
                 "documenti sul sito di EmaNews.</i>"
        ),
        NotificationBy.TELEGRAM: TelegramNotification(
            text="💊 <b>Lo stato di un medicinale è cambiato. Ecco le informazioni aggiornate:</b>\n"
                 "🔸 <b>Nome latino:</b> {latin_name}\n"
                 "🔸 <b>Nome botanico:</b> {botanic_name}\n"
                 "🔸 <b>Nome inglese:</b> {english_name}\n"
                 "🔸 <b>Nuovo stato:</b> <code>{status}</code>\n"
                 "\n<i>Puoi consultare la lista completa delle erbe e dei relativi "
                 "documenti sul sito di EmaNews.</i>",
            keyboard=[[{"text": "🔗 Consulta", "url": "{url}"}]]
        )
    },
    NotificationWhen.DOCUMENT_UPDATE: {
        NotificationBy.EMAIL: EmailNotification(
            subject="EmaNews: Documento aggiornato",
            html="<h4>Un documento è stato aggiornato. Ecco le nuove informazioni:</h4>"
                 "<ul>"
                 "<li><b>Nome:</b> {name}</li>"
                 "<li><b>Tipo:</b> {type}</li>"
                 "<li><b>Erba:</b> {latin_name} ~ {botanic_name} ~ {english_name}</li>"
                 "<li><b>URL:</b> {url}</li>"
                 "</ul>"
                 "<i>Puoi consultare la lista completa delle erbe e dei relativi "
                 "documenti sul sito di EmaNews.</i>"
        ),
        NotificationBy.TELEGRAM: TelegramNotification(
            text="📄 <b>Un documento è stato aggiornato. Ecco le nuove informazioni:</b>\n"
                 "🔸 <b>Nome:</b> {name}\n"
                 "🔸 <b>Tipo:</b> {type}\n"
                 "🔸 <b>Erba:</b> {latin_name} ~ {botanic_name} ~ {english_name}\n"
                 "\n<i>Puoi consultare la lista completa delle erbe e dei relativi "
                 "documenti sul sito di EmaNews.</i>",
            keyboard=[[{"text": "🔗 Consulta", "url": "{url}"}]]
        )
    }
}
