# -*- coding: utf-8 -*-
from typing import Type

from .http import HttpRequest

from ..conf import settings


class ItemTypesClient:

    hostname = settings.API_HOSTNAME

    def get_item_types(
        self: Type,
        token: str,
    ) -> bool:

        url = f'{self.hostname}/api/item-types/'

        return HttpRequest(
            url=url,
            method='GET',
            headers={'Authorization': f'Bearer {token}'},
            format='request',
        ).request
