# -*- coding: utf-8 -*-
from django.test import TestCase

from .test_base import BaseTestCase


class TenantItemsViewSetTestCase(BaseTestCase):

    def test_unauthenticated_list(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/items/'

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

        url = f'/api/tenants/{self.tenant_aaa.id}/items/{self.item_aaa.id}/'

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

        url = f'/api/tenants/{self.tenant_aaa.id}/items/'

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

        url = f'/api/tenants/{self.tenant_aaa.id}/items/{self.item_aaa.id}/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_list_filters(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/items/'

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
            url + '?item_type=flat-page',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        request = self.client.get(
            url + '?item_type=',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        request = self.client.get(
            url + '?item_type=flat-page2&item_type=news2',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        request = self.client.get(
            url + '?item_type=flat-page&item_type=news',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_create_flat_page(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/items/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            url,
            {
                'item_type': 'flat-page',
                'tenant': self.tenant_aaa.id,
                'translatable_content': [{
                    'title': 'Test Aaa',
                    'slug': 'test-aaa',
                    'content': 'test aaa content'
                }],
                'parent_items': [{
                    'parent_id': self.item_aaa.id,
                    'label': 'previous-page'
                }]
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

    def test_authenticated_create_and_update_flat_page(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/items/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            url,
            {
                'item_type': 'flat-page',
                'tenant': self.tenant_aaa.id,
                'translatable_content': [{
                    'title': 'Test Aaa',
                    'slug': 'test-aaa',
                    'content': 'test aaa content'
                }],
                'parent_items': [{
                    'parent_id': self.item_aaa.id,
                    'label': 'previous-page'
                }]
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        parent_items = request.json()['parent_items']

        self.assertEquals(
            len(parent_items),
            1
        )

        request = self.client.post(
            url,
            {
                'item_type': 'flat-page',
                'tenant': self.tenant_aaa.id,
                'translatable_content': [{
                    'title': 'Test Aaa Aaa',
                    'slug': 'test-aaa-aaa',
                    'content': 'test aaa content'
                }],
                'parent_items': []
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        parent_items = request.json()['parent_items']

        self.assertEquals(
            len(parent_items),
            0
        )

    def test_authenticated_create_inaccessible_item_type(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/items/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            url,
            {
                'item_type': 'news',
                'tenant': self.tenant_aaa.id,
                'translatable_content': [{
                    'title': 'Test Aaa',
                    'slug': 'test-aaa',
                    'content': 'test aaa content'
                }],
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

    def test_authenticated_create_and_update_change_tenant(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/items/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            url,
            {
                'item_type': 'flat-page',
                'tenant': self.tenant_aaa.id,
                'translatable_content': [{
                    'title': 'Test Aaa',
                    'slug': 'test-aaa',
                    'content': 'test aaa content'
                }]
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        request = self.client.post(
            url,
            {
                'item_type': 'flat-page',
                'tenant': self.tenant_bbb.id,
                'translatable_content': [{
                    'title': 'Test Aaa',
                    'slug': 'test-aaa',
                    'content': 'test aaa content'
                }]
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

    def test_authenticated_create_and_destroy(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/items/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            url,
            {
                'item_type': 'flat-page',
                'tenant': self.tenant_aaa.id,
                'translatable_content': [{
                    'title': 'Test Aaa',
                    'slug': 'test-aaa',
                    'content': 'test aaa content'
                }]
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        data = request.json()

        request = self.client.delete(
            url + f'{data["id"]}/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            204
        )
