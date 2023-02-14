# -*- coding: utf-8 -*-
from typing import Type

from .http import HttpRequest

from ..conf import settings


class UsersClient:

    hostname = settings.API_HOSTNAME

    def get_user(
        self: Type,
        token: str,
        user_pk: int,
    ) -> bool:

        url = f'{self.hostname}/api/users/{user_pk}/'

        return HttpRequest(
            url=url,
            method='GET',
            headers={'Authorization': f'Bearer {token}'},
            format='request',
        ).request
