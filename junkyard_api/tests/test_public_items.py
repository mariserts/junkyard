# -*- coding: utf-8 -*-
from django.test import TestCase

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
