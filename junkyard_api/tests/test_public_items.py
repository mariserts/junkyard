# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase

from ..conf import settings

from .test_base import BaseTestCase


class PublicItemsViewSetTestCase(BaseTestCase):

    def test_list(
        self: TestCase,
    ) -> None:

        request = self.client.get(
            '/api/public-items/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_retrieve(
        self: TestCase,
    ) -> None:

        request = self.client.get(
            f'/api/public-items/{self.item_aaa.id}/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        request = self.client.get(
            '/api/public-items/1000/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            404
        )

    def test_creation(
        self: TestCase,
    ) -> None:

        request = self.client.post(
            '/api/public-items/',
            {},
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_retrieve_not_found_published_no_published_at(
        self: TestCase,
    ) -> None:

        request = self.client.get(
            f'/api/public-items/{self.item_bbb.id}/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            404
        )

    def test_retrieve_not_found_unpublished_no_published_at(
        self: TestCase,
    ) -> None:

        request = self.client.get(
            f'/api/public-items/{self.item_ccc.id}/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            404
        )

    def test_retrieve_not_found(
        self: TestCase,
    ) -> None:

        request = self.client.get(
            '/api/public-items/1000/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            404
        )

    def test_create_and_filter_list_by_filter(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        url = f'/api/tenants/{self.tenant_aaa.id}/items/'

        self.authenticate_with_token(self.token_aaa)

        published_at = datetime.datetime.now(datetime.timezone.utc)
        published_at += datetime.timedelta(hours=-1)

        request = self.client.post(
            url,
            {
                'item_type': 'flat-page',
                'tenant': self.tenant_aaa.id,
                'translatable_content': [{
                    'title': 'Test Aaaaaaaaaaaaa',
                    'slug': 'test-aaa',
                    'content': 'test aaa content',
                    'language': settings.LANGUAGE_DEFAULT,
                }],
                'published': True,
                'published_at': published_at
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        data = request.json()

        request = self.client.get(
            '/api/public-items/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        data_2 = request.json()

        self.assertEquals(
            data_2['total'],
            2
        )

        url = '/api/public-items/'
        url += '?filter=translatable_content__title:'
        url += f'{data["translatable_content"][0]["title"]}'
        url += f'&item_type={data["item_type"]}'

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        data_3 = request.json()

        self.assertEquals(
            data_3['total'],
            1
        )

        self.assertEquals(
            data_3['results'][0]['translatable_content'][0]['title'],
            data['translatable_content'][0]['title']
        )

    def test_create_and_filter_list_by_filter_icontains(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        url = f'/api/tenants/{self.tenant_aaa.id}/items/'

        self.authenticate_with_token(self.token_aaa)

        published_at = datetime.datetime.now(datetime.timezone.utc)
        published_at += datetime.timedelta(hours=-1)

        request = self.client.post(
            url,
            {
                'item_type': 'flat-page',
                'tenant': self.tenant_aaa.id,
                'translatable_content': [{
                    'title': 'Test Aaaaaaaaaaaaa',
                    'slug': 'test-aaa',
                    'content': 'test aaa content',
                    'language': settings.LANGUAGE_DEFAULT,
                }],
                'published': True,
                'published_at': published_at
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        data = request.json()

        request = self.client.get(
            '/api/public-items/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        data_2 = request.json()

        self.assertEquals(
            data_2['total'],
            2
        )

        url = '/api/public-items/'
        url += '?filter=translatable_content__title__icontains:'
        url += f'{data["translatable_content"][0]["title"]}'
        url += f'&item_type={data["item_type"]}'

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        data_3 = request.json()

        self.assertEquals(
            data_3['total'],
            1
        )

        self.assertEquals(
            data_3['results'][0]['translatable_content'][0]['title'],
            data['translatable_content'][0]['title']
        )
