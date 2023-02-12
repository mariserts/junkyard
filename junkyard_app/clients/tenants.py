# -*- coding: utf-8 -*-
from typing import List, Type, Union

from .http import HttpRequest

from ..conf import settings


class TenantsClient:

    hostname = settings.API_HOSTNAME

    def get_tenants(
        self: Type,
        token: str,
        project_pk: int,
        page: int = 1,
        count: int = 10,
        user_id: Union[None, str, int] = None,
        item_types: List[str] = [],
    ) -> bool:

        url = f'{self.hostname}/api/projects/{project_pk}/tenants/'
        url += f'?page={page}'
        url += f'&count={count}'

        return HttpRequest(
            url=url,
            method='GET',
            headers={'Authorization': f'Bearer {token}'},
            format='request',
        ).request
