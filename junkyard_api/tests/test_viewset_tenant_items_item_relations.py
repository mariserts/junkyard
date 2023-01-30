# -*- coding: utf-8 -*-
from django.test import TestCase

from rest_framework.test import APIClient

from ..models import Item, ItemRelation, Tenant, User


class TenantItemsItemRelationsViewSetTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create(
            email='TenantItemsItemRelationsViewSetTestCase@test.com'
        )

        self.tenant = Tenant.objects.create(
            owner=self.user,
            translatable_content=[{'language': 'en', 'title': 'Test'}],
            is_active=True,
        )

        self.item = Item.objects.create(
            tenant=self.tenant,
            item_type='flat-page',
            translatable_content=[{
                'language': 'en',
                'title': 'Test',
                'content': 'Test',
            }],
        )

        self.item_bbb = Item.objects.create(
            tenant=self.tenant,
            item_type='flat-page',
            translatable_content=[{
                'language': 'en',
                'title': 'Test_Bbb',
                'content': 'Test Bbb',
            }],
        )

        self.relation = ItemRelation.objects.create(
            parent=self.item_bbb,
            child=self.item,
            label='Label'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_relations(self):

        request = self.client.get(
            f'/api/tenants/{self.tenant.id}/items/{self.item.id}/relations/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )
