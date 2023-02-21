# -*- coding: utf-8 -*-
from typing import Type, Union

from ..utils.urls import get_projects_items_url

from .test_base import BaseTestCase


class ProjectsItemsViewSetTestCase(
    BaseTestCase
):

    def setUp(self):

        super().setUp()

        self.item_data = {
            'project': self.project_one.id,
            'data': {
                'translatable_content': [{
                    'language': 'en',
                    'title': '1',
                    'slug': 'en-1',
                    'content': 'Hello world!'
                }]
            },
        }

    def get_url(
        self: Type,
        project_pk: Union[str, int],
        item_pk: Union[None, int] = None,
    ):
        return get_projects_items_url(None, project_pk, item_pk)

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


class AuthenticatedProjectsItemsViewSetTestCase(
    ProjectsItemsViewSetTestCase
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
