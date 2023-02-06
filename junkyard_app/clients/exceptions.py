# -*- coding: utf-8 -*-
class ClientException(Exception):
    def __init__(self, msg, status_code=500):
        self.msg = msg
        self.status_code = status_code
        super().__init__(msg)


class HTTPError(ClientException):
    pass


class ClientWarning(Warning):
    pass


class ClientRequestError(ClientException):
    pass


class UpStreamServerError(ClientException):
    pass


class JSONParsingError(UpStreamServerError):
    pass
