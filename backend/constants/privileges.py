from enum import auto, IntFlag


class Privileges(IntFlag):
    NONE = 0
    PENDING_ACTIVATION = auto()
    NORMAL = auto()
    ADMIN = auto()
