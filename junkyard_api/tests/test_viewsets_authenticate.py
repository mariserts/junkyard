# -*- coding: utf-8 -*-
from .test_base import BaseTestCase


class AuthenticateViewSetTestCase(
    BaseTestCase
):

    pass

    # def test_sign_in(
    #     self: Type
    # ):
    #
    #     request = self.client.post(
    #         '/api/authenticate/sign-in/',
    #         {
    #             'email': self.user_one_email,
    #             'password': self.user_one_password
    #         },
    #         format='json'
    #     )
    #
    #     self.assertEquals(
    #         request.status_code,
    #         201
    #     )
    #
    #     self.assertIn(
    #         'user',
    #         request.json()
    #     )
