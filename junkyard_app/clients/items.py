# -*- coding: utf-8 -*-
from typing import List, Type

from .http import HttpClient

from ..conf import settings


class ItemsClient:

    hostname = settings.API_HOSTNAME

    def get_items(
        self: Type,
        token: str,
        page: int = 1,
        count: int = 10,
        item_types: List[str] = [],
    ) -> bool:

        url = f'{self.hostname}/api/items/'
        url += f'?page={page}'
        url += f'&count={count}'

        return HttpClient(
            url=url,
            method='GET',
            headers={'Authorization': f'Bearer {token}'},
            format='request',
        ).request
