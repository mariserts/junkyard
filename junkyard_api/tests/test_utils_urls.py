# -*- coding: utf-8 -*-
from typing import Type

from django.test import TestCase

from ..utils.urls import (
    get_cryptography_url,
    get_projects_item_types_url,
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

    def test_get_projects_item_types_url(
        self: Type
    ) -> None:

        url = get_projects_item_types_url(
            None,
            1
        )

        self.assertEquals(
            url,
            '/api/projects/1/item-types/'
        )

        url = get_projects_item_types_url(
            None,
            1,
            'news'
        )

        self.assertEquals(
            url,
            '/api/projects/1/item-types/news/'
        )

    def test_get_cryptography_url(
        self: Type
    ) -> None:

        url = get_cryptography_url(
            None,
        )

        self.assertEquals(
            url,
            '/api/cryptography/sign/'
        )

        url = get_cryptography_url(
            None,
            False
        )

        self.assertEquals(
            url,
            '/api/cryptography/unsign/'
        )
