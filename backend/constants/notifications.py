from enum import IntFlag, auto


class NotificationEvents(IntFlag):
    NONE = 0
    NEW_MEDICINE = auto()
    MEDICINE_UPDATE = auto()
    NEW_DOCUMENT = auto()
    DOCUMENT_UPDATE = auto()


class NotificationBy(IntFlag):
    NONE = 0
    EMAIL = auto()
    TELEGRAM = auto()
