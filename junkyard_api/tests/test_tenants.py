# -*- coding: utf-8 -*-
from django.test import TestCase

from ..models import Tenant, User

from .test_base import BaseTestCase


class TenantsViewSetTestCase(BaseTestCase):

    def test_unauthenticated_list(self):

        request = self.client.get(
            '/api/tenants/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_unauthenticated_retrieve(self):

        url = f'/api/tenants/{self.tenant_aaa.id}/'

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_authenticated_list(self):

        url = '/api/tenants/'

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token_aaa.token}'
        )

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

    def test_authenticated_retrieve(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token_aaa.token}'
        )

        url = f'/api/tenants/{self.tenant_aaa.id}/'

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_list_filter_test(self):

        url = '/api/tenants/'

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token_aaa.token}'
        )

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

    def test_authenticated_retrieve_no_permission(self):

        """ UserAaa should not see TenantBbb (2) """

        url = f'/api/tenants/{self.tenant_bbb.id}/'

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token_aaa.token}'
        )

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            403
        )

    def test_authenticated_retrieve_as_admin(self):

        """ UserBbb is admin for TenantAaa (1) """

        url = f'/api/tenants/{self.tenant_aaa.id}/'

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token_bbb.token}'
        )

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )


class TenantsHierarchyTestCase(TestCase):

    def test_tenant_hierarchy(self):

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
