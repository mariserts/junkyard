# -*- coding: utf-8 -*-
from typing import Type, Union

from ..models import ProjectTenantUser, ProjectTenant, ProjectUser
from ..utils.urls import get_projects_tenants_items_url

from .test_base import BaseTestCase


class ProjectsTenantsItemsViewSetTestCase(
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
        tenant_pk: Union[str, int],
        item_pk: Union[None, str, int] = None,
    ):
        return get_projects_tenants_items_url(
            None, project_pk, tenant_pk, item_pk)

    def test_list_view(
        self: Type
    ):

        request = self.client.get(
            self.get_url(self.project_one.id, self.tenant_one.id),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )


class AuthenticatedProjectsTenantsItemsViewSetTestCase(
    ProjectsTenantsItemsViewSetTestCase
):

    def test_list_view(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        request = self.client.get(
            self.get_url(self.project_one.id, self.tenant_one.id),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_create_view_user_not_project_tenant_user(
        self: Type
    ):

        data = self.item_data.copy()
        data['item_type'] = self.item_type_news.code
        data['tenant'] = self.tenant_one.id

        self.authenticate_with_token(self.access_token_one)

        request = self.client.post(
            self.get_url(self.project_one.id, self.tenant_one.id),
            data,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            403
        )

    def test_create_view_user_project_tenant_user(
        self: Type
    ):

        ProjectTenant.objects.create(
            project=self.project_one,
            tenant=self.tenant_one,
        )

        ProjectTenantUser.objects.create(
            project=self.project_one,
            tenant=self.tenant_one,
            user=self.user_one
        )

        data = self.item_data.copy()
        data['item_type'] = self.item_type_news.code
        data['tenant'] = self.tenant_one.id

        self.authenticate_with_token(self.access_token_one)

        request = self.client.post(
            self.get_url(self.project_one.id, self.tenant_one.id),
            data,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

    def test_create_view_user_project_user(
        self: Type
    ):

        ProjectTenant.objects.create(
            project=self.project_one,
            tenant=self.tenant_one,
        )

        ProjectUser.objects.create(
            project=self.project_one,
            user=self.user_one
        )

        data = self.item_data.copy()
        data['item_type'] = self.item_type_news.code
        data['tenant'] = self.tenant_one.id

        self.authenticate_with_token(self.access_token_one)

        request = self.client.post(
            self.get_url(self.project_one.id, self.tenant_one.id),
            data,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

    def test_create_view_no_item_type_access(
        self: Type
    ):

        ProjectTenant.objects.create(
            project=self.project_one,
            tenant=self.tenant_one,
        )

        ProjectTenantUser.objects.create(
            project=self.project_one,
            tenant=self.tenant_one,
            user=self.user_one
        )

        data = self.item_data.copy()
        data['item_type'] = self.item_type_flat_page.code
        data['tenant'] = self.tenant_one.id

        self.authenticate_with_token(self.access_token_one)

        request = self.client.post(
            self.get_url(self.project_one.id, self.tenant_one.id),
            data,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

    def test_create_view_crud(
        self: Type
    ):

        ProjectTenant.objects.create(
            project=self.project_one,
            tenant=self.tenant_one,
        )

        ProjectTenantUser.objects.create(
            project=self.project_one,
            tenant=self.tenant_one,
            user=self.user_one
        )

        data = self.item_data.copy()
        data['item_type'] = self.item_type_news.code
        data['tenant'] = self.tenant_one.id

        self.authenticate_with_token(self.access_token_one)

        # C
        request = self.client.post(
            self.get_url(self.project_one.id, self.tenant_one.id),
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
            self.get_url(self.project_one.id, self.tenant_one.id, item_id),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        # U
        request = self.client.put(
            self.get_url(self.project_one.id, self.tenant_one.id, item_id),
            data,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        request = self.client.patch(
            self.get_url(self.project_one.id, self.tenant_one.id, item_id),
            data,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        # D
        request = self.client.delete(
            self.get_url(self.project_one.id, self.tenant_one.id, item_id),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            204
        )
