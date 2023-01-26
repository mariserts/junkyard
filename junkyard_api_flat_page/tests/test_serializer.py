# -*- coding: utf-8 -*-
from django.test import TestCase

from junkyard_api.conf import settings as junkyard_api_settings
from junkyard_api.models import Tenant, User

from ..conf import settings
from ..serializers import FlatPageSerializer


class FlatPageSerializerTestCase(TestCase):

    CONTENT = {
        'language': junkyard_api_settings.LANGUAGE_DEFAULT,
        'title': 'Hello world',
        'content': 'First flat page'
    }

    def test_validation(self):

        user = User.objects.create(
            email='test@test.com',
            username='test@test.com'
        )

        tenant = Tenant.objects.create(
            owner=user
        )

        data = {
            'item_type': settings.ITEM_TYPE,
            'tenant': tenant.id,
            'translatable_content': [
                self.CONTENT
            ]
        }

        serializer = FlatPageSerializer(data=data)

        self.assertEquals(
            serializer.is_valid(),
            True
        )

    def test_failed_validation(self):

        user = User.objects.create(
            email='test@test.com',
            username='test@test.com'
        )

        tenant = Tenant.objects.create(
            owner=user
        )

        content = self.CONTENT.copy()
        content.pop('title')

        data = {
            'item_type': settings.ITEM_TYPE,
            'tenant': tenant.id,
            'translatable_content': [
                content
            ]
        }

        serializer = FlatPageSerializer(data=data)

        self.assertEquals(
            serializer.is_valid(),
            False
        )

    def test_failed_item_type(self):

        user = User.objects.create(
            email='test@test.com',
            username='test@test.com'
        )

        tenant = Tenant.objects.create(
            owner=user
        )

        data = {
            'item_type': '-1',
            'tenant': tenant.id,
            'translatable_content': [
                self.CONTENT
            ]
        }

        serializer = FlatPageSerializer(data=data)

        self.assertEquals(
            serializer.is_valid(),
            False
        )
