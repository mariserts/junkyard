# -*- coding: utf-8 -*-
from django.test import TestCase

from ..models import Tenant, User

from .test_base import BaseTestCase


class TenantsViewSetTestCase(BaseTestCase):

    def test_unauthenticated_list(
        self: TestCase,
    ) -> None:

        request = self.client.get(
            '/api/tenants/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_unauthenticated_retrieve(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/'

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_authenticated_list(
        self: TestCase,
    ) -> None:

        url = '/api/tenants/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        request = self.client.get(
            url + f'?successor_of={self.tenant_aaa.id}',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_retrieve(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        url = f'/api/tenants/{self.tenant_aaa.id}/'

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_list_filter_test(
        self: TestCase,
    ) -> None:

        url = '/api/tenants/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.get(
            url + f'?predecessors_of={self.tenant_aaa.id}',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        request = self.client.get(
            url + f'?all_predecessors_of={self.tenant_aaa.id}',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        request = self.client.get(
            url + f'?successors_of={self.tenant_aaa.id}',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        request = self.client.get(
            url + f'?all_successors_of={self.tenant_aaa.id}',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        request = self.client.get(
            url + '?is_root=true',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_retrieve_no_permission(
        self: TestCase,
    ) -> None:

        """ UserAaa should not see TenantBbb (2) """

        url = f'/api/tenants/{self.tenant_bbb.id}/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            403
        )

    def test_authenticated_retrieve_as_admin(
        self: TestCase,
    ) -> None:

        """ UserBbb is admin for TenantAaa (1) """

        url = f'/api/tenants/{self.tenant_aaa.id}/'

        self.authenticate_with_token(self.token_bbb)

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_update(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        url = f'/api/tenants/{self.tenant_aaa.id}/'

        request = self.client.patch(
            url,
            {
                'parent': self.tenant_aaa.parent,
                'translatable_content': [{
                    'language': 'en',
                    'title': 'Test Aaa Aaa'
                }]
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_update_no_translatable_content(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        url = f'/api/tenants/{self.tenant_aaa.id}/'

        request = self.client.patch(
            url,
            {
                'parent': self.tenant_aaa.parent,
                'translatable_content': []
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )


class TenantsHierarchyTestCase(TestCase):

    def test_tenant_hierarchy(
        self: TestCase,
    ) -> None:

        user = User.objects.create(email='TenantsHierarchyTestCase@test.case')

        tenant_aaa = Tenant.objects.create(
            owner=user,
            translatable_content=[{'language': 'en', 'title': 'aaa'}],
            is_active=True,
        )
        tenant_bbb = Tenant.objects.create(
            owner=user,
            parent=tenant_aaa,
            translatable_content=[{'language': 'en', 'title': 'bbb'}],
            is_active=True,
        )
        tenant_ccc = Tenant.objects.create(
            owner=user,
            parent=tenant_bbb,
            translatable_content=[{'language': 'en', 'title': 'ccc'}],
            is_active=True,
        )
        tenant_ddd = Tenant.objects.create(
            owner=user,
            parent=tenant_ccc,
            translatable_content=[{'language': 'en', 'title': 'ddd'}],
            is_active=True,
        )

        children = Tenant.get_all_children_ids(tenant_aaa, use_cache=False)

        self.assertEquals(
            len(children),
            3
        )

        parents = Tenant.get_all_parents(tenant_ddd)

        self.assertEquals(
            len(parents),
            3
        )

        parents = Tenant.get_all_parents(tenant_aaa)

        self.assertEquals(
            len(parents),
            0
        )
