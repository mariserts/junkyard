# -*- coding: utf-8 -*-
from rest_framework import serializers

from junkyard_api.serializers.items import BaseItemSerializer

from .conf import settings


class ThingCategoryTranslatableContentSerializer(
    serializers.Serializer
):

    language = language = serializers.CharField()
    title = serializers.CharField()
    content = serializers.CharField()


class ThingCategoryDataSerializer(
    serializers.Serializer
):

    translatable_content = ThingCategoryTranslatableContentSerializer(
        many=True)


class ThingCategorySerializer(
    BaseItemSerializer
):

    item_type = serializers.CharField(default=settings.ITEM_TYPE)
    data = ThingCategoryDataSerializer()
