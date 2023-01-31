# -*- coding: utf-8 -*-
from django.test import TestCase

from .test_base import BaseTestCase


class TenantAdminViewSetTestCase(BaseTestCase):

    def test_unauthenticated_list(
        self: TestCase,
    ) -> None:

        request = self.client.get(
            f'/api/tenants/{self.tenant_aaa.id}/admins/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_unauthenticated_retrieve(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'admins/{self.tenant_admin_aaa.id}/'

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
            f'/api/tenants/{self.tenant_aaa.id}/admins/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_retrieve(
        self: TestCase,
    ) -> None:

        url = f'/api/tenants/{self.tenant_aaa.id}/'
        url += f'admins/{self.tenant_admin_aaa.id}/'

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

        url = f'/api/tenants/{self.tenant_aaa.id}/admins/'

        self.authenticate_with_token(self.token_aaa)

        request = self.client.get(
            url + f'?email={self.user_bbb.email}',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_list_no_premission(
        self: TestCase,
    ) -> None:

        """ User (1) should not see Tenant (2) """

        self.authenticate_with_token(self.token_aaa)

        request = self.client.get(
            f'/api/tenants/{self.tenant_bbb.id}/admins/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            403
        )

    def test_authenticated_create(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            f'/api/tenants/{self.tenant_aaa.id}/admins/',
            {
                'tenant': self.token_aaa.id,
                'user': self.user_aaa.id,
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

    def test_authenticated_create_missing_tenant(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            f'/api/tenants/{self.tenant_aaa.id}/admins/',
            {
                'user': self.user_aaa.id,
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

    def test_authenticated_create_switching_tenants(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            f'/api/tenants/{self.tenant_aaa.id}/admins/',
            {
                'tenant': self.token_bbb.id,
                'user': self.user_aaa.id,
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

    def test_authenticated_create_and_update(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            f'/api/tenants/{self.tenant_aaa.id}/admins/',
            {
                'tenant': self.token_aaa.id,
                'user': self.user_aaa.id,
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        data = request.json()

        request = self.client.patch(
            f'/api/tenants/{self.tenant_aaa.id}/admins/{data["id"]}/',
            {
                'tenant': self.token_aaa.id,
                'user': self.user_aaa.id,
                'label': 'admin'
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_authenticated_create_and_update_switch_tenants(
        self: TestCase,
    ) -> None:

        self.authenticate_with_token(self.token_aaa)

        request = self.client.post(
            f'/api/tenants/{self.tenant_aaa.id}/admins/',
            {
                'tenant': self.token_aaa.id,
                'user': self.user_aaa.id,
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        data = request.json()

        request = self.client.patch(
            f'/api/tenants/{self.tenant_aaa.id}/admins/{data["id"]}/',
            {
                'tenant': self.token_bbb.id,
                'user': self.user_aaa.id,
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )
