# -*- coding: utf-8 -*-
from django.test import TestCase

from .test_base import BaseTestCase


class TenantItemItemRelationsViewSetTestCase(BaseTestCase):

    def test_unauthenticated_list(
        self: TestCase,
    ) -> None:

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

    def test_unauthenticated_retrieve(
        self: TestCase,
    ) -> None:

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

    def test_authenticated_list(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'items/{self.item_aaa.id}/relations/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_retrieve(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'items/{self.item_aaa.id}/relations/{self.relation_aaa.id}/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_retrieve_not_found(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'items/{self.item_aaa.id}/relations/1000/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            404
        )

    def test_authenticated_create(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'items/{self.item_aaa.id}/relations/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            url,
            {
                'parent': self.item_bbb.id,
                'child': self.item_aaa.id,
                'label': 'xd'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

    def test_authenticated_create_and_update(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'items/{self.item_aaa.id}/relations/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            url,
            {
                'parent': self.item_bbb.id,
                'child': self.item_aaa.id,
                'label': 'xd'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        data = request.json()

        request = self.client.patch(
            url + f'{data["id"]}/',
            {
                'parent': self.item_bbb.id,
                'child': self.item_aaa.id,
                'label': 'xdxd'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_create_and_update_child_not_matching(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'items/{self.item_aaa.id}/relations/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            url,
            {
                'parent': self.item_bbb.id,
                'child': self.item_aaa.id,
                'label': 'xd'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        data = request.json()

        request = self.client.patch(
            url + f'{data["id"]}/',
            {
                'parent': self.item_bbb.id,
                'child': self.item_bbb.id,
                'label': 'xdxd'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

    def test_authenticated_create_payload_child_not_matching(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'items/{self.item_aaa.id}/relations/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            url,
            {
                'parent': self.item_bbb.id,
                'child': self.item_bbb.id,
                'label': 'xd'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )
