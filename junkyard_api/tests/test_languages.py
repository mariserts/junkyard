# -*- coding: utf-8 -*-
from django.test import TestCase

from ..conf import settings

from .test_base import BaseTestCase


class LanguagesViewSetTestCase(BaseTestCase):

    def test_unauthenticated_list(
        self: TestCase,
    ) -> None:

        request = self.client.get(
            '/api/languages/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_unauthenticated_retrieve(
        self: TestCase,
    ) -> None:

        request = self.client.get(
            f'/api/languages/{settings.LANGUAGE_DEFAULT}/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_authenticated_list(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        request = self.client.get(
            '/api/languages/',
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

        request = self.client.get(
            f'/api/languages/{settings.LANGUAGE_DEFAULT}/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_retrieve_not_found(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        fake_language = settings.LANGUAGE_DEFAULT + 'aaa'

        request = self.client.get(
            f'/api/languages/{fake_language}/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            404
        )

    def test_authenticated_list_filter_default(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        request = self.client.get(
            '/api/languages/?default=true',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        data = request.json()

        self.assertEquals(
            data['total'],
            1
        )

        self.assertEquals(
            data['results'][0]['code'],
            settings.LANGUAGE_DEFAULT
        )
