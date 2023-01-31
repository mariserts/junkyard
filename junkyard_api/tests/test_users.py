# -*- coding: utf-8 -*-
from .test_base import BaseTestCase


class UsersViewSetTestCase(BaseTestCase):

    def test_unauthenticated_list(self):

        request = self.client.get(
            '/api/users/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_unauthenticated_retrieve(self):

        url = f'/api/users/{self.user_aaa.id}/'

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_authenticated_list(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token_aaa.token}'
        )

        request = self.client.get(
            '/api/users/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_retrieve(self):

        url = f'/api/users/{self.user_aaa.id}/'

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token_aaa.token}'
        )

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_list_filters(self):

        url = '/api/users/'

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token_aaa.token}'
        )

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
