# -*- coding: utf-8 -*-
from typing import Type, Union

from .http import HttpRequest

from ..conf import settings


class ItemTypesClient:

    hostname = settings.API_HOSTNAME

    def get_project_item_types(
        self: Type,
        token: str,
        project_pk: int,
        for_user: Union[int, None] = None,
    ) -> dict:

        url = f'{self.hostname}/api/projects/{project_pk}/item-types/?'

        if for_user is not None:
            url += f'&for_user={for_user}'

        return HttpRequest(
            url=url,
            method='GET',
            headers={'Authorization': f'Bearer {token}'},
            format='request',
        ).request
