# -*- coding: utf-8 -*-
from .test_base import BaseTestCase


class PublicItemsViewSetTestCase(BaseTestCase):

    def test_list(self):

        request = self.client.get(
            '/api/public-items/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_retrieve(self):

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

    def test_retrieve_not_found_published_no_published_at(self):

        request = self.client.get(
            f'/api/public-items/{self.item_bbb.id}/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            404
        )

    def test_retrieve_not_found_unpublished_no_published_at(self):

        request = self.client.get(
            f'/api/public-items/{self.item_ccc.id}/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            404
        )

    def test_retrieve_not_found(self):

        request = self.client.get(
            '/api/public-items/1000/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            404
        )
