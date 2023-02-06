# -*- coding: utf-8 -*-
from typing import Type

from .http import HttpClient

from ..conf import settings


class AuthenticationClient:

    hostname = settings.API_HOSTNAME

    def register(
        self: Type,
        email: str,
        password: str,
    ) -> dict:

        return HttpClient(
            url=f'{self.hostname}/api/authenticate/register/',
            method='POST',
            data={
                'email': email,
                'password': password,
            },
        ).request

    def sign_in(
        self: Type,
        email: str,
        password: str,
    ) -> dict:

        return HttpClient(
            url=f'{self.hostname}/api/authenticate/sign-in/',
            method='POST',
            data={
                'email': email,
                'password': password,
            },
        ).request

    def sign_out(
        self: Type,
        token: str
    ) -> bool:

        return HttpClient(
            url=f'{self.hostname}/api/authenticate/sign-out/',
            method='POST',
            data={'token': token},
            headers={'Authorization': f'Bearer {token}'},
            format='request',
        ).request
