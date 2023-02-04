# -*- coding: utf-8 -*-
from django.test import TestCase

from .test_base import BaseTestCase


class UsersViewSetTestCase(BaseTestCase):

    def test_unauthenticated_list(
        self: TestCase,
    ) -> None:

        request = self.client.get(
            '/api/users/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_unauthenticated_retrieve(
        self: TestCase,
    ) -> None:

        url = f'/api/users/{self.user_aaa.id}/'

        request = self.client.get(
            url,
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
            '/api/users/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_retrieve(
        self: TestCase,
    ) -> None:

        url = f'/api/users/{self.user_aaa.id}/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_retrieve_other_user(
        self: TestCase,
    ) -> None:

        url = f'/api/users/{self.user_bbb.id}/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_list_filters(
        self: TestCase,
    ) -> None:

        url = '/api/users/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.get(
            url + f'?email={self.user_aaa.email}',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        request = self.client.get(
            url + f'?admin_of={self.tenant_aaa.id}',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        request = self.client.get(
            url + f'?owner_of={self.tenant_bbb.id}',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    # def test_unauthenticated_create(
    #     self: TestCase,
    # ) -> None:
    #
    #     url = '/api/users/'
    #
    #     request = self.client.post(
    #         url,
    #         {
    #             'email': 'test@test.case',
    #             'password': 'HelloWorld123!'
    #         },
    #         format='json'
    #     )
    #
    #     self.assertEquals(
    #         request.status_code,
    #         201
    #     )

    # def test_unauthenticated_create_no_email_no_password(
    #     self: TestCase,
    # ) -> None:
    #
    #     url = '/api/users/'
    #
    #     request = self.client.post(
    #         url,
    #         {
    #             'email': 'test@test.case',
    #         },
    #         format='json'
    #     )
    #
    #     self.assertEquals(
    #         request.status_code,
    #         400
    #     )
    #
    #     request = self.client.post(
    #         url,
    #         {
    #             'password': 'HelloWorld123!',
    #         },
    #         format='json'
    #     )
    #
    #     self.assertEquals(
    #         request.status_code,
    #         400
    #     )

    # def test_authenticated_create_duplicates(
    #     self: TestCase,
    # ) -> None:
    #
    #     url = '/api/users/'
    #
    #     request = self.client.post(
    #         url,
    #         {
    #             'email': 'test@test.case',
    #             'password': 'HelloWorld123!'
    #         },
    #         format='json'
    #     )
    #
    #     self.assertEquals(
    #         request.status_code,
    #         201
    #     )
    #
    #     request = self.client.post(
    #         url,
    #         {
    #             'email': 'test@test.case',
    #             'password': 'HelloWorld123!'
    #         },
    #         format='json'
    #     )
    #
    #     self.assertEquals(
    #         request.status_code,
    #         400
    #     )

    # def test_authenticated_create_bad_email(
    #     self: TestCase,
    # ) -> None:
    #
    #     url = '/api/users/'
    #
    #     request = self.client.post(
    #         url,
    #         {
    #             'email': 'test.case',
    #             'password': 'HelloWorld123!'
    #         },
    #         format='json'
    #     )
    #
    #     self.assertEquals(
    #         request.status_code,
    #         400
    #     )

    # def test_authenticated_create_bad_password(
    #     self: TestCase,
    # ) -> None:
    #
    #     url = '/api/users/'
    #
    #     request = self.client.post(
    #         url,
    #         {
    #             'email': 'test@test.case',
    #             'password': '123456'
    #         },
    #         format='json'
    #     )
    #
    #     self.assertEquals(
    #         request.status_code,
    #         400
    #     )

    # def test_authenticated_set_password(
    #     self: TestCase,
    # ) -> None:
    #
    #     url = f'/api/users/{self.token_aaa.id}/set-password/'
    #
    #     self.authenticate_with_token(self.token_aaa)
    #
    #     request = self.client.post(
    #         url,
    #         {
    #             'password': 'HelloWorld123!!'
    #         },
    #         format='json'
    #     )
    #
    #     self.assertEquals(
    #         request.status_code,
    #         200
    #     )

    # def test_authenticated_set_bad_password(
    #     self: TestCase,
    # ) -> None:
    #
    #     url = f'/api/users/{self.token_aaa.id}/set-password/'
    #
    #     self.authenticate_with_token(self.token_aaa)
    #
    #     request = self.client.post(
    #         url,
    #         {
    #             'password': '123456'
    #         },
    #         format='json'
    #     )
    #
    #     self.assertEquals(
    #         request.status_code,
    #         400
    #     )

    # def test_authenticated_set_no_password(
    #     self: TestCase,
    # ) -> None:
    #
    #     url = f'/api/users/{self.token_aaa.id}/set-password/'
    #
    #     self.authenticate_with_token(self.token_aaa)
    #
    #     request = self.client.post(
    #         url,
    #         {},
    #         format='json'
    #     )
    #
    #     self.assertEquals(
    #         request.status_code,
    #         400
    #     )

    # def test_authenticated_set_password_to_someone_else(
    #     self: TestCase,
    # ) -> None:
    #
    #     url = f'/api/users/{self.token_bbb.id}/set-password/'
    #
    #     self.authenticate_with_token(self.token_aaa)
    #
    #     request = self.client.post(
    #         url,
    #         {
    #             'password': 'HelloWorld123!!'
    #         },
    #         format='json'
    #     )
    #
    #     self.assertEquals(
    #         request.status_code,
    #         403
    #     )
