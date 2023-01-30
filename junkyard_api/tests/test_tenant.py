# -*- coding: utf-8 -*-
from django.test import TestCase

from ..models import Tenant, User


class TenantGetAllChildrenTestCase(TestCase):

    def test_one(self):

        user = User.objects.create(email='test@test.com')

        tenant_aaa = Tenant.objects.create(
            owner=user,
            translatable_content=[{'language': 'en', 'title': 'aaa'}],
            is_active=True,
        )
        tenant_bbb = Tenant.objects.create(
            owner=user,
            parent=tenant_aaa,
            translatable_content=[{'language': 'en', 'title': 'bbb'}],
            is_active=True,
        )
        tenant_ccc = Tenant.objects.create(
            owner=user,
            parent=tenant_bbb,
            translatable_content=[{'language': 'en', 'title': 'ccc'}],
            is_active=True,
        )
        tenant_ddd = Tenant.objects.create(
            owner=user,
            parent=tenant_ccc,
            translatable_content=[{'language': 'en', 'title': 'ddd'}],
            is_active=True,
        )

        children = Tenant.get_all_children_ids(tenant_aaa)

        self.assertEquals(
            len(children),
            3
        )

        parents = Tenant.get_all_parents(tenant_ddd)

        self.assertEquals(
            len(parents),
            3
        )

        parents = Tenant.get_all_parents(tenant_aaa)

        self.assertEquals(
            len(parents),
            0
        )
