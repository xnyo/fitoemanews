from typing import Optional

from constants.notifications import EmailNotification
from singletons.emanews import EmaNews


async def send_notification(email_address: str, notification: EmailNotification, fmt: Optional[dict]=None):
    fmt = {} if fmt is None else fmt
    await EmaNews().mailgun_client.send(
        to=email_address,
        subject=notification.subject,
        html=notification.html.format(**fmt)
    )

