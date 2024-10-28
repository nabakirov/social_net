

class AbstractBaseException(Exception):
    message: str = None
    detail: any = None
    default_message: str = 'Base exception'

    def __init__(self, message: str = None, detail: any = None):
        self.message = message or self.default_message
        self.detail = detail

    def __str__(self):
        return f'msg: {self.message}\n detail: {self.detail}'


class InvalidResponse(AbstractBaseException):
    default_message = 'Received invalid response'


class Unauthorized(AbstractBaseException):
    message = 'unauthorized'


class Forbidden(AbstractBaseException):
    message = 'forbidden'


class NotFound(AbstractBaseException):
    message = 'received 404 status code'


class AuthenticationFailed(AbstractBaseException):
    message = 'authentication failed'


class TooManyRequests(AbstractBaseException):
    message = 'флуд запросов'

