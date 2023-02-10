# -*- coding: utf-8 -*-
from typing import Type, Union

from .test_base import BaseTestCase


class ProjectsUsersViewSetTestCase(
    BaseTestCase
):

    def get_url(
        self: Type,
        project_pk: Union[str, int]
    ):
        return f'/api/projects/{project_pk}/users/'

    def test_list_view(
        self: Type
    ):

        request = self.client.get(
            self.get_url(self.project_one.id),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )


class AuthenticatedProjectsUsersViewSetTestCase(
    ProjectsUsersViewSetTestCase
):

    def test_list_view(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        request = self.client.get(
            self.get_url(self.project_one.id),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )
