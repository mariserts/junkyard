# -*- coding: utf-8 -*-
from typing import Type, Union

from ..utils.urls import get_projects_item_types_url

from .test_base import BaseTestCase


class ProjectsItemTypesViewSetTestCase(
    BaseTestCase
):

    def get_url(
        self: Type,
        project_pk: Union[str, int]
    ):
        return get_projects_item_types_url(None, project_pk)

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


class AuthenticatedProjectsItemTypesViewSetTestCase(
    ProjectsItemTypesViewSetTestCase
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
