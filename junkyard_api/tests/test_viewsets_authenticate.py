# -*- coding: utf-8 -*-
from typing import Type
from unittest.mock import patch

from .test_base import BaseTestCase


class AuthenticateViewSetTestCase(
    BaseTestCase
):

    def setUp(self):
        super().setUp()
        self.mock_request = patch(
            'junkyard_api.viewsets.authenticate.requests.post'
        )
        self.mock_post = self.mock_request.start()

    def tearDown(self):
        self.mock_request.stop()
        super().tearDown()

    def test_register(
        self: Type
    ):

        self.mock_post.return_value.status_code = 201
        self.mock_post.return_value.ok = True
        self.mock_post.return_value.json.return_value = {}

        request = self.client.post(
            '/api/authenticate/register/',
            {
                'email': 'user_four@test.case',
                'password': 'abcd1234!'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        self.assertIn(
            'user',
            request.json()
        )

    def test_sign_in(
        self: Type
    ):

        self.mock_post.return_value.status_code = 201
        self.mock_post.return_value.ok = True
        self.mock_post.return_value.json.return_value = {}

        request = self.client.post(
            '/api/authenticate/sign-in/',
            {
                'email': self.user_one_email,
                'password': self.user_one_password
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        self.assertIn(
            'user',
            request.json()
        )
