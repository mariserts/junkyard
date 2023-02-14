# -*- coding: utf-8 -*-
from typing import Type

from django.test import TestCase

from junkyard_api_news.registry_entry import NewsRegistryEntry

from ..models import Item, ItemRelation, ItemType, Project
from ..serializers.items import BaseItemSerializer, ItemSerializer


class BaseItemSerializertTestCase(
    TestCase
):

    def setUp(self):

        self.project_one = Project.objects.create(name='One')
        self.item_type = ItemType.objects.get(code=NewsRegistryEntry.code)

        self.data = {
            'id': None,
            'project': self.project_one.id,
            'tenant': None,
            'moved_to': None,
            'item_type': self.item_type.code,
            'metadata': {},
            'translatable_content': [],
            'parent_items': [],
            'archived': False,
            'archived_at': None,
            'published': False,
            'published_at': None
        }

    def tearDown(self):
        Project.objects.all().delete()


class BaseItemSerializerTestCase(
    BaseItemSerializertTestCase
):

    def test_one(
        self: Type,
    ) -> None:

        serializer = BaseItemSerializer(data=self.data)

        is_valid = serializer.is_valid()

        self.assertIs(
            is_valid,
            True
        )


class ItemSerializerTestOneCase(
    BaseItemSerializertTestCase
):

    def test_one(
        self: Type,
    ) -> None:

        serializer = ItemSerializer(data=self.data)

        is_valid = serializer.is_valid()

        self.assertIs(
            is_valid,
            True
        )

    def test_two(
        self: Type,
    ) -> None:

        serializer = ItemSerializer(data=self.data)

        is_valid = serializer.is_valid()

        self.assertIs(
            is_valid,
            True
        )

        serializer.save()

        self.assertEquals(
            Item.objects.all().count(),
            1
        )

    def test_create_items_with_relations(
        self: Type,
    ) -> None:

        serializer = ItemSerializer(data=self.data)

        is_valid = serializer.is_valid()

        self.assertIs(
            is_valid,
            True
        )

        serializer.save()

        self.assertEquals(
            Item.objects.all().count(),
            1
        )

        data_two = self.data.copy()
        data_two['parent_items'] = [{
            'parent': 1,
            'child': None,
            'label': 'successor',
        }]

        serializer = ItemSerializer(data=data_two)

        is_valid = serializer.is_valid()

        self.assertIs(
            is_valid,
            True
        )

        serializer.save()

        self.assertEquals(
            Item.objects.all().count(),
            2
        )

        self.assertEquals(
            ItemRelation.objects.all().count(),
            1
        )
