# -*- coding: utf-8 -*-
from .test_base import BaseTestCase


class TenantItemTypeViewSetTestCase(BaseTestCase):

    def test_unauthenticated_list(self):

        request = self.client.get(
            f'/api/tenants/{self.tenant_aaa.id}/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_unauthenticated_retrieve(self):

        request = self.client.get(
            f'/api/tenants/{self.tenant_aaa.id}/item-types/',
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
            f'/api/tenants/{self.tenant_aaa.id}/',
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

        request = self.client.get(
            f'/api/tenants/{self.tenant_aaa.id}/item-types/flat-page/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )
