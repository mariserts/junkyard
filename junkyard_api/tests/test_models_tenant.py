# -*- coding: utf-8 -*-
from typing import Type

from django.test import TestCase

from ..models import Tenant


class TenantModelTestCase(TestCase):

    def setUp(
        self: Type
    ) -> None:

        self.tenant_one = Tenant.objects.create(
            is_active=True
        )

        self.tenant_two = Tenant.objects.create(
            parent=self.tenant_one,
            is_active=True
        )

        self.tenant_three = Tenant.objects.create(
            parent=self.tenant_two,
            is_active=True
        )

        self.tenant_four = Tenant.objects.create(
            parent=self.tenant_three,
            is_active=True
        )

        self.tenant_five = Tenant.objects.create(
            parent=self.tenant_one,
            is_active=True
        )

    def tearDown(
        self: Type
    ) -> None:
        Tenant.objects.all().delete()

    def test_get_all_children_one(
        self: Type
    ) -> None:
        self.assertEquals(
            self.tenant_one.get_all_children().count(),
            4
        )

    def test_get_all_children_two(
        self: Type
    ) -> None:
        self.assertEquals(
            self.tenant_two.get_all_children().count(),
            2
        )

    def test_get_all_children_three(
        self: Type
    ) -> None:
        self.assertEquals(
            self.tenant_three.get_all_children().count(),
            1
        )

    def test_get_all_children_four(
        self: Type
    ) -> None:
        self.assertEquals(
            self.tenant_four.get_all_children().count(),
            0
        )
