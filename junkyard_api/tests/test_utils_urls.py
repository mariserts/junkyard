# -*- coding: utf-8 -*-
from typing import Type

from django.test import TestCase

from ..utils.urls import (
    get_cryptography_url,
    get_projects_tenants_items_url
)


class UtilsUrlsTestCase(
    TestCase
):

    def test_get_projects_tenants_items_url(
        self: Type
    ) -> None:

        url = get_projects_tenants_items_url(
            None,
            1,
            1,
        )

        self.assertEquals(
            url,
            '/api/projects/1/tenants/1/items/'
        )

        url = get_projects_tenants_items_url(
            None,
            1,
            1,
            item_pk=1
        )

        self.assertEquals(
            url,
            '/api/projects/1/tenants/1/items/1/'
        )

    def get_cryptography_url(
        self: Type
    ) -> None:

        url = get_cryptography_url(
            None,
            True,
        )

        self.assertEquals(
            url,
            '/api/crypthography/sign/'
        )

        url = get_cryptography_url(
            None,
        )

        self.assertEquals(
            url,
            '/api/crypthography/unsign/'
        )
