# -*- coding: utf-8 -*-
from .test_base import BaseTestCase


class TenantAdminViewSetTestCase(BaseTestCase):

    def test_unauthenticated_list(self):

        request = self.client.get(
            f'/api/tenants/{self.tenant_aaa.id}/admins/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_unauthenticated_retrieve(self):

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'admins/{self.tenant_admin_aaa.id}/'

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_authenticated_list(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token_aaa.token}'
        )

        request = self.client.get(
            f'/api/tenants/{self.tenant_aaa.id}/admins/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_retrieve(self):

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'admins/{self.tenant_admin_aaa.id}/'

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

    def test_authenticated_list_filters(self):

        url = f'/api/tenants/{self.tenant_aaa.id}/admins/'

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token_aaa.token}'
        )

        request = self.client.get(
            url + f'?email={self.user_bbb.email}',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_list_no_premission(self):

        """ User (1) should not see Tenant (2) """

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token_aaa.token}'
        )

        request = self.client.get(
            f'/api/tenants/{self.tenant_bbb.id}/admins/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            403
        )
