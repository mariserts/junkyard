# -*- coding: utf-8 -*-
from typing import Type, Union

from ..models import ProjectUser

from .test_base import BaseTestCase


class ProjectsItemsViewSetTestCase(
    BaseTestCase
):

    def setUp(self):

        super().setUp()

        self.item_data = {
            'metadata': {},
            'project': self.project_one.id,
            'translatable_content': [{
                'content': 'data',
                'language': 'en',
                'title': 'data',
                'slug': 'data'
            }],
        }

    def get_url(
        self: Type,
        project_pk: Union[str, int]
    ):
        return f'/api/projects/{project_pk}/items/'

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

    def test_create_view_user_not_project_user(
        self: Type
    ):

        data = self.item_data.copy()
        data['item_type'] = self.item_type_flat_page.code
        data['tenant'] = None

        self.authenticate_with_token(self.access_token_one)

        request = self.client.post(
            self.get_url(self.project_one.id),
            data,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            403
        )

    def test_create_view_user_project_user(
        self: Type
    ):

        ProjectUser.objects.create(
            project=self.project_one,
            user=self.user_one
        )

        data = self.item_data.copy()
        data['item_type'] = self.item_type_flat_page.code
        data['tenant'] = None

        self.authenticate_with_token(self.access_token_one)

        request = self.client.post(
            self.get_url(self.project_one.id),
            data,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )
