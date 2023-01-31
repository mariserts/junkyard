# -*- coding: utf-8 -*-
from .test_base import BaseTestCase


class TenantItemItemRelationsViewSetTestCase(BaseTestCase):

    def test_unauthenticated_list(self):

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'items/{self.item_aaa.id}/relations/'

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_unauthenticated_retrieve(self):

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'items/{self.item_aaa.id}/relations/{self.relation_aaa.id}/'

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_authenticated_list(self):

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'items/{self.item_aaa.id}/relations/'

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

    def test_authenticated_retrieve(self):

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'items/{self.item_aaa.id}/relations/{self.relation_aaa.id}/'

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

    def test_authenticated_retrieve_not_found(self):

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'items/{self.item_aaa.id}/relations/1000/'

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token_aaa.token}'
        )

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            404
        )
