"""
Eccezioni API
"""

class NotFoundError(Exception):
    pass


class InternalServerError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class MissingArgumentsError(Exception):
    pass


class InvalidArgumentsError(Exception):
    pass


class ConflictError(Exception):
    pass


class Created(Exception):
    pass


class ForceLogoutError(Exception):
    pass


class Ok(Exception):
    pass


class NotAcceptableError(Exception):
    pass


class NotAuthenticatedError(Exception):
    pass
