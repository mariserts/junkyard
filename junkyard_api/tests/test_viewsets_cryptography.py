# -*- coding: utf-8 -*-
from typing import Type

from .test_base import BaseTestCase


class CryptographyViewSetTestCase(
    BaseTestCase
):

    def get_sign_url(
        self: Type,
    ):
        return '/api/cryptography/sign/'

    def get_unsign_url(
        self: Type,
    ):
        return '/api/cryptography/unsign/'

    def test_sign_view(
        self: Type
    ):

        request = self.client.post(
            self.get_sign_url(),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_unsign_view(
        self: Type
    ):

        request = self.client.post(
            self.get_unsign_url(),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )


class AuthenticatedCryptographyViewSetTestCase(
    CryptographyViewSetTestCase
):

    def test_sign_view(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        request = self.client.post(
            self.get_sign_url(),
            {
                'data': 'hello',
                'max_age': 20,
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

    def test_unsign_view(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        request = self.client.post(
            self.get_sign_url(),
            {
                'data': 'hello',
                'max_age': 20,
            },
            format='json'
        )

        data = request.json()

        request = self.client.post(
            self.get_unsign_url(),
            {
                'signature': data['signature']
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )
