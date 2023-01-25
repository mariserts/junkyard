from django.test import TestCase

from ...serializers.items import ItemSerializer
from .constants import ITEM


class ItemSerializerTestCase(TestCase):

    def test_one(self):

        serializer = ItemSerializer(data=ITEM)

        valid = serializer.is_valid()

        print(serializer.errors)

        self.assertEquals(
            valid,
            True
        )
