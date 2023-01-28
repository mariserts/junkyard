# -*- coding: utf-8 -*-
from django.test import TestCase

from rest_framework.test import APIClient

from ..models import Item, ItemRelation, Tenant, TenantAdmin, User


class TenantItemsViewSetTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='TenantItemsViewSetTestCase@test.com'
        )
        self.user_bbb = User.objects.create(
            email='TenantItemsViewSetTestBbbCase@test.com'
        )
        self.tenant = Tenant.objects.create(
            owner=self.user,
            translatable_content=[{'language': 'en', 'title': 'Test'}]
        )
        self.tenant_bbb = Tenant.objects.create(
            owner=self.user_bbb,
            translatable_content=[{'language': 'en', 'title': 'TestBbb'}]
        )
        self.tenant_ccc = Tenant.objects.create(
            owner=self.user_bbb,
            translatable_content=[{'language': 'en', 'title': 'TestCcc'}]
        )

        TenantAdmin.objects.create(
            tenant=self.tenant_ccc,
            user=self.user,
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_accessing_tenant(self):

        request = self.client.get(
            f'/api/tenants/{self.tenant.id}/items/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        request = self.client.get(
            f'/api/tenants/{self.tenant_bbb.id}/items/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            403
        )

        request = self.client.get(
            f'/api/tenants/{self.tenant_ccc.id}/items/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_item_creation(self):

        request = self.client.post(
            f'/api/tenants/{self.tenant.id}/items/',
            {
                'item_type': 'flat-page',
                'tenant': self.tenant.id,
                'translatable_content': [{
                    'language': 'en',
                    'title': 'test',
                    'content': 'test'
                }]
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        request = self.client.post(
            f'/api/tenants/{self.tenant.id}/items/',
            {
                'item_type': 'flat-page',
                'tenant': self.tenant_bbb.id,
                'translatable_content': [{
                    'language': 'en',
                    'title': 'test',
                    'content': 'test'
                }]
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

    def test_item_update(self):

        request = self.client.post(
            f'/api/tenants/{self.tenant.id}/items/',
            {
                'item_type': 'flat-page',
                'tenant': self.tenant.id,
                'translatable_content': [{
                    'language': 'en',
                    'title': 'test',
                    'content': 'test'
                }]
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        request = self.client.patch(
            f'/api/tenants/{self.tenant.id}/items/1/',
            {
                'item_type': 'flat-page',
                'tenant': self.tenant.id,
                'translatable_content': [{
                    'language': 'en',
                    'title': 'Test',
                    'content': 'Test'
                }]
            },
            format='json'
        )

        self.assertEquals(
            Item.objects.all().first().translatable_content[0]['title'],
            'Test'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        request = self.client.patch(
            f'/api/tenants/{self.tenant.id}/items/1/',
            {
                'item_type': 'flat-page',
                'tenant': self.tenant_bbb.id,
                'translatable_content': [{
                    'language': 'en',
                    'title': 'test',
                    'content': 'test'
                }]
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            400
        )

    def test_item_deletion(self):

        request = self.client.post(
            f'/api/tenants/{self.tenant.id}/items/',
            {
                'item_type': 'flat-page',
                'tenant': self.tenant.id,
                'translatable_content': [{
                    'language': 'en',
                    'title': 'test',
                    'content': 'test'
                }]
            },
            format='json'
        )

        self.assertEquals(
            request.status_code,
            201
        )

        request = self.client.delete(
            f'/api/tenants/{self.tenant.id}/items/1/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            204
        )

        self.assertEquals(
            Item.objects.all().count(),
            0
        )

    def test_item_relations_creation(self):

        self.client.post(
            f'/api/tenants/{self.tenant.id}/items/',
            {
                'item_type': 'flat-page',
                'tenant': self.tenant.id,
                'translatable_content': [{
                    'language': 'en',
                    'title': 'Test',
                    'content': 'Test'
                }]
            },
            format='json'
        )

        self.client.post(
            f'/api/tenants/{self.tenant.id}/items/',
            {
                'item_type': 'flat-page',
                'tenant': self.tenant.id,
                'translatable_content': [{
                    'language': 'en',
                    'title': 'TestBbb',
                    'content': 'TestBbb'
                }]
            },
            format='json'
        )

        self.client.patch(
            f'/api/tenants/{self.tenant.id}/items/1/',
            {
                'item_type': 'flat-page',
                'tenant': self.tenant.id,
                'translatable_content': [{
                    'language': 'en',
                    'title': 'Test',
                    'content': 'Test'
                }],
                'parent_items': [{
                    'parent': 2,
                    'label': 'Label'
                }]
            },
            format='json'
        )

        self.assertEquals(
            ItemRelation.objects.all().count(),
            1
        )

        self.client.patch(
            f'/api/tenants/{self.tenant.id}/items/1/',
            {
                'item_type': 'flat-page',
                'tenant': self.tenant.id,
                'translatable_content': [{
                    'language': 'en',
                    'title': 'Test',
                    'content': 'Test'
                }],
                'parent_items': [{
                    'id': 1,
                    'parent': 2,
                    'label': 'Label2'
                }]
            },
            format='json'
        )

        self.assertEquals(
            ItemRelation.objects.all().first().label,
            'Label2'
        )

        self.assertEquals(
            ItemRelation.objects.all().count(),
            1
        )

        self.client.patch(
            f'/api/tenants/{self.tenant.id}/items/1/',
            {
                'item_type': 'flat-page',
                'tenant': self.tenant.id,
                'translatable_content': [{
                    'language': 'en',
                    'title': 'Test',
                    'content': 'Test'
                }],
                'parent_items': []
            },
            format='json'
        )

        self.assertEquals(
            ItemRelation.objects.all().count(),
            0
        )
