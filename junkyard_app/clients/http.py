# -*- coding: utf-8 -*-
from typing import Union, Type

import requests

from .exceptions import (
    ClientRequestError,
    ClientWarning,
    UpStreamServerError,
    HTTPError,
    JSONParsingError,
)

default_session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=1)
default_session.mount('https://', adapter)
default_session.mount('http://', adapter)


class HttpRequest:

    def __init__(
        self: Type,
        session: Union[None, requests.Session] = default_session,
        **kwargs: dict,
    ) -> None:

        self.kwargs = kwargs

        if session is None:
            session = requests.Session()

        self.session = session

    @property
    def default_headers(
        self: Type,
    ) -> str:

        return {
            'Content-type': 'application/json'
        }

    @property
    def format(
        self: Type,
    ) -> str:

        return self.kwargs.get('format', 'json').lower()

    @property
    def headers(
        self: Type,
    ) -> dict:

        headers = self.kwargs.get('headers', {})
        headers.update(self.default_headers)

        return headers

    @property
    def method(
        self: Type,
    ) -> str:

        return self.kwargs.get('method', 'get').lower()

    @property
    def request(
        self: Type,
    ) -> Union[requests.models.Request, dict]:

        try:
            request = self.session.request(
                self.method,
                self.url,
                json=self.kwargs.get('data', {}),
                headers=self.headers
            )
            request.raise_for_status()

        except ValueError as error:
            raise ClientRequestError(error)

        except requests.exceptions.HTTPError:
            if request.status_code == 500:
                raise HTTPError('Upstream ServerError500', request.status_code)
            raise HTTPError(request.text, request.status_code)

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

    @property
    def url(
        self: Type,
    ) -> str:

        return self.kwargs.get('url', '')
