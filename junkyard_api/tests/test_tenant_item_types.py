# -*- coding: utf-8 -*-
from django.test import TestCase

from .test_base import BaseTestCase


class TenantItemTypeViewSetTestCase(BaseTestCase):

    def test_unauthenticated_list(
        self: TestCase,
    ) -> None:

        request = self.client.get(
            f'/api/tenants/{self.tenant_aaa.id}/',
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
            f'/api/tenants/{self.tenant_aaa.id}/item-types/',
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
            f'/api/tenants/{self.tenant_aaa.id}/',
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
            f'/api/tenants/{self.tenant_aaa.id}/item-types/flat-page/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )
