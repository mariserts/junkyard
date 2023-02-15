# -*- coding: utf-8 -*-
import time

from typing import Type

from ..utils.urls import get_cryptography_url

from .test_base import BaseTestCase


class CryptographyViewSetTestCase(
    BaseTestCase
):

    DATA = {
        'data': 'hello',
        'max_age': 20,
    }

    def get_sign_url(
        self: Type,
    ):
        return get_cryptography_url(None)

    def get_unsign_url(
        self: Type,
    ):
        return get_cryptography_url(None, False)

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
            self.DATA,
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
            self.DATA,
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

    def test_sign_view_no_data(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        request = self.client.post(
            self.get_sign_url(),
            {
                'max_age': 20,
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

    def test_unsign_view_no_signature(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        request = self.client.post(
            self.get_unsign_url(),
            {},
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

    def test_unsign_view_bad_signature(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        request = self.client.post(
            self.get_unsign_url(),
            {
                'signature': '1'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

        request = self.client.post(
            self.get_unsign_url(),
            {
                'signature': '1::2'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

    def test_unsign_view_expired(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        data = self.DATA.copy()
        data['max_age'] = 1

        request = self.client.post(
            self.get_sign_url(),
            data,
            format='json'
        )

        time.sleep(1)

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
            400
        )

    def test_unsign_view_bad_max_age(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        request = self.client.post(
            self.get_sign_url(),
            self.DATA,
            format='json'
        )

        data = request.json()

        sig = data['signature'].split('::')[1]

        signature = f'{sig}::{sig}'

        request = self.client.post(
            self.get_unsign_url(),
            {
                'signature': signature
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )
