# -*- coding: utf-8 -*-
from typing import Type

from .http import HttpRequest

from ..conf import settings


class TenantsClient:

    hostname = settings.API_HOSTNAME

    def get_project_tenants(
        self: Type,
        token: str,
        project_pk: int,
    ) -> dict:

        url = f'{self.hostname}/api/projects/{project_pk}/tenants/?'

        return HttpRequest(
            url=url,
            method='GET',
            headers={'Authorization': f'Bearer {token}'},
            format='request',
        ).request
