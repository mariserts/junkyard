# -*- coding: utf-8 -*-
from typing import Type

from django.test import TestCase

from ..utils.urls import get_projects_tenants_items_url


class UtilsUrlsGetProjectsTenantsItemsUrlTestCase(
    TestCase
):

    def test_one(
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
