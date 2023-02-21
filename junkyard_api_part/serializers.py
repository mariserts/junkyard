# -*- coding: utf-8 -*-
from rest_framework import serializers

from junkyard_api.serializers.items import BaseItemSerializer

from .conf import settings


class PartTranslatableContentSerializer(
    serializers.Serializer
):

    language = language = serializers.CharField()
    title = serializers.CharField()
    content = serializers.CharField()


class PartDataSerializer(
    serializers.Serializer
):

    available = serializers.IntegerField(required=False, default=0)
    currency = serializers.CharField()
    price = serializers.DecimalField(decimal_places=2, max_digits=20)
    translatable_content = PartTranslatableContentSerializer(many=True)


class PartSerializer(
    BaseItemSerializer
):

    item_type = serializers.CharField(default=settings.ITEM_TYPE)
    data = PartDataSerializer()
