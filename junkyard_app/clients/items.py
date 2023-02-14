# -*- coding: utf-8 -*-
from typing import Type, Union

from .http import HttpRequest

from ..conf import settings


class ItemsClient:

    hostname = settings.API_HOSTNAME

    def get_items(
        self: Type,
        token: str,
        project_pk: int,
        page: int = 1,
        count: int = 10,
        action: Union[str, None] = None
    ) -> bool:

        url = f'{self.hostname}/api/projects/{project_pk}/items/'
        url += f'?page={page}'
        url += f'&count={count}'

        if action is not None:
            url += f'&action={action}'

        return HttpRequest(
            url=url,
            method='GET',
            headers={'Authorization': f'Bearer {token}'},
            format='request',
        ).request
