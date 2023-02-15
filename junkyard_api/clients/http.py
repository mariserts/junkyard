# -*- coding: utf-8 -*-
from typing import Union, Type

import requests

from .exceptions import (
    ClientRequestError,
    ClientWarning,
    HTTPError,
    UpStreamServerError,
    JSONParsingError,
)


default_session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=1)
default_session.mount('https://', adapter)
default_session.mount('http://', adapter)


class HttpRequest:

    def __init__(
        self: Type,
        session: Union[None, Type[requests.Session]] = default_session,
    ) -> None:

        if session is None:
            session = requests.Session()

        self.session = session

    def request(
        self: Type,
        data: Union[dict, None] = None,
        format: str = 'request',
        headers: dict = {},
        method: str = 'get',
        url: str = '',
    ) -> Union[requests.models.Request, dict]:

        _headers = headers.copy()
        _headers.update({'Content-type': 'application/json'})

        _method = str(method).lower()

        try:
            request = self.session.request(
                _method,
                url,
                json=data,
                headers=_headers
            )
            request.raise_for_status()

        except ValueError as error:
            raise ClientRequestError(error)

        except requests.exceptions.HTTPError:
            if request.status_code == 500:
                raise HTTPError('Upstream ServerError500', request.status_code)

        except requests.exceptions.ConnectionError as error:
            raise UpStreamServerError(error, request.status_code)

        except requests.exceptions.Timeout as error:
            raise UpStreamServerError(error, request.status_code)

        except requests.exceptions.RequestException as error:
            raise UpStreamServerError(error, request.status_code)

        except requests.exceptions.RequestsWarning as warning:
            raise ClientWarning(warning)

        if format == 'request':
            return request

        try:
            data = request.json()

        except requests.exceptions.InvalidJSONError as error:
            raise JSONParsingError(error)

        return data
