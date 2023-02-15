# -*- coding: utf-8 -*-
from typing import Type, Union

from ..models import ProjectUser
from ..utils.urls import get_projects_items_url

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

    def test_create_view_crud(
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

        # C
        request = self.client.post(
            self.get_url(self.project_one.id),
            data,
            format='json'
        )

        item_data = request.json()
        item_id = str(item_data['id'])

        self.assertEquals(
            request.status_code,
            201
        )

        # R
        request = self.client.get(
            self.get_url(self.project_one.id, item_id),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        # U
        request = self.client.put(
            self.get_url(self.project_one.id, item_id),
            data,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        request = self.client.patch(
            self.get_url(self.project_one.id, item_id),
            data,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        # D
        request = self.client.delete(
            self.get_url(self.project_one.id, item_id),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            204
        )
