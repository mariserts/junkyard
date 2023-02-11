# -*- coding: utf-8 -*-
from typing import Type

from .test_base import BaseTestCase


class LanguagesViewSetTestCase(
    BaseTestCase
):

    def get_url(
        self: Type,
    ):
        return '/api/languages/'

    def test_list_view(
        self: Type
    ):

        request = self.client.get(
            self.get_url(),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )


class AuthenticatedLanguagesViewSetTestCase(
    LanguagesViewSetTestCase
):

    def test_list_view(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        request = self.client.get(
            self.get_url(),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )
