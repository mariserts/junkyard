# -*- coding: utf-8 -*-
from typing import Type

from .http import HttpRequest

from ..conf import settings


class ProjectsClient:

    hostname = settings.API_HOSTNAME

    def get_projects(
        self: Type,
        token: str,
        page: int = 1,
        count: int = 10,
    ) -> bool:

        url = f'{self.hostname}/api/projects/'
        url += f'?page={page}'
        url += f'&count={count}'

        return HttpRequest(
            url=url,
            method='GET',
            headers={'Authorization': f'Bearer {token}'},
            format='request',
        ).request
