# -*- coding: utf-8 -*-
from typing import Any, Type

from rest_framework.response import Response

from ..clients.http import HttpRequest


class ProxyMixin:

    def _proxy(
        self: Type,
        url: str,
        method: str = None,
        data: Any = None,
        headers: Any = None,
    ) -> Type[Response]:

        if method is None:
            method = self.request.method

        if data is None:
            data = self.request.data

        if headers is None:
            headers = self.request.META

        request = HttpRequest().request(
            data=data,
            format='request',
            headers=headers,
            method=method,
            url=url
        )

        if request.ok() is True:

            return Response(
                request.json(),
                status=request.status_code
            )

        return Response(
            request.text,
            status=request.status_code
        )

    def _get_full_request_hostname(
        self: Type,
    ) -> str:
        hostname = 'http'
        if self.request.is_secure is True:
            hostname += 's'
        hostname += '://'
        hostname += self.request.get_host()
        return hostname
