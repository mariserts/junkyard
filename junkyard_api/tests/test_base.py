# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase

from rest_framework.test import APIClient

from oauth2_provider.models import AccessToken

from ..models import (
    Application,
    Item,
    ItemRelation,
    Tenant,
    TenantAdmin,
    User
)


class BaseTestCase(TestCase):

    def setUp(
        self: TestCase,
    ) -> None:

        aaa_email = 'BaseTestCaseAaa@test.case'
        aaa_password = 'aaaa'

        self.user_aaa = User.objects.create(
            email=aaa_email,
            is_superuser=True,
        )

        self.user_aaa.set_password(aaa_password)
        self.user_aaa.save()

        self.user_bbb = User.objects.create(
            email='BaseTestCaseBbb@test.case'
        )

        self.tenant_aaa = Tenant.objects.create(
            owner=self.user_aaa,
            translatable_content=[{
                'language': 'en',
                'title': 'Test Aaa'
            }],
            is_active=True,
        )

        self.tenant_bbb = Tenant.objects.create(
            owner=self.user_bbb,
            translatable_content=[{
                'language': 'en',
                'title': 'Test Bbb'
            }],
            is_active=True,
        )

        self.tenant_admin_aaa = TenantAdmin.objects.create(
            tenant=self.tenant_aaa,
            user=self.user_bbb
        )

        published_at = datetime.datetime.now(datetime.timezone.utc)
        published_at += datetime.timedelta(hours=-1)

        self.item_aaa = Item.objects.create(
            tenant=self.tenant_aaa,
            item_type='flat-page',
            translatable_content=[{
                'language': 'en',
                'title': 'Test Aaa',
                'slug': 'test-aaa',
                'content': 'test aaa'
            }],
            published=True,
            published_at=published_at,
        )

        self.item_bbb = Item.objects.create(
            tenant=self.tenant_aaa,
            item_type='flat-page',
            translatable_content=[{
                'language': 'en',
                'title': 'Test Bbb',
                'slug': 'test-bbb',
                'content': 'test bbb'
            }],
            published=True,
        )

        self.item_ccc = Item.objects.create(
            tenant=self.tenant_aaa,
            item_type='flat-page',
            translatable_content=[{
                'language': 'en',
                'title': 'Test Ccc',
                'slug': 'test-ccc',
                'content': 'test ccc'
            }],
        )

        self.relation_aaa = ItemRelation.objects.create(
            parent=self.item_bbb,
            child=self.item_aaa,
            label='next-page'
        )

        self.client = APIClient()

        self.application_aaa = Application.objects.filter(
            user=self.user_aaa
        ).first()

        self.application_bbb = Application.objects.filter(
            user=self.user_aaa
        ).first()

        expires = datetime.datetime.now(datetime.timezone.utc)
        expires += datetime.timedelta(hours=1)

        self.token_aaa = AccessToken.objects.create(
            user=self.user_aaa,
            scope='read write',
            token='aaa',
            expires=expires
        )

        self.token_bbb = AccessToken.objects.create(
            user=self.user_bbb,
            scope='read write',
            token='bbb',
            expires=expires
        )

    def tearDown(
        self: TestCase,
    ) -> None:
        User.objects.all().delete()

    def authenticate_with_token(
        self: TestCase,
        token: AccessToken,
    ) -> None:

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token.token}'
        )
