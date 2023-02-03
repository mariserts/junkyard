# -*- coding: utf-8 -*-
import time

from django.test import TestCase

from .test_base import BaseTestCase


class SigningViewSetTestCase(BaseTestCase):

    def test_unauthenticated_sign(
        self: TestCase,
    ) -> None:

        request = self.client.post(
            '/api/signer/sign/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_unauthenticated_unsign(
        self: TestCase,
    ) -> None:

        request = self.client.post(
            '/api/signer/unsign/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_authenticated_sign(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            '/api/signer/sign/',
            {
                'data': {
                    'x': 'y'
                },
                'max_age': None,
                'salt': 'xyz'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

    def test_authenticated_sign_unsign_with_max_age(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            '/api/signer/sign/',
            {
                'data': {
                    'x': 'y'
                },
                'max_age': 10,
                'salt': 'xyz'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        data = request.json()

        request = self.client.post(
            '/api/signer/unsign/',
            {
                'signature': data['signature'],
                'salt': 'xyz',
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        data = request.json()

        self.assertEquals(
            data['data']['x'],
            'y'
        )

    def test_authenticated_sign_unsign(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            '/api/signer/sign/',
            {
                'data': {
                    'x': 'y'
                },
                'salt': 'xyz',
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        data = request.json()

        request = self.client.post(
            '/api/signer/unsign/',
            {
                'signature': data['signature'],
                'salt': 'xyz',
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        data = request.json()

        self.assertEquals(
            data['data']['x'],
            'y'
        )

    def test_authenticated_sign_unsign_exipred_signature(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            '/api/signer/sign/',
            {
                'data': {
                    'x': 'y'
                },
                'max_age': 1,
                'salt': 'xyz'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        time.sleep(1)

        data = request.json()

        request = self.client.post(
            '/api/signer/unsign/',
            {
                'signature': data['signature'],
                'salt': 'xyz',
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

    def test_authenticated_sign_max_age_not_int(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            '/api/signer/sign/',
            {
                'data': {
                    'x': 'y'
                },
                'max_age': 'a',
                'salt': 'xyz'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

    def test_authenticated_sign_no_data(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            '/api/signer/sign/',
            {
                'max_age': None,
                'salt': 'xyz'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

    def test_authenticated_unsign_no_data(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            '/api/signer/unsign/',
            {
                'max_age': None,
                'salt': 'xyz'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

    def test_authenticated_unsign_bad_signature(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            '/api/signer/unsign/',
            {
                'data': 'abc',
                'max_age': None,
                'salt': 'xyz'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )
