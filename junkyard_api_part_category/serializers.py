# -*- coding: utf-8 -*-
from rest_framework import serializers

from junkyard_api.serializers.items import BaseItemSerializer

from .conf import settings


class PartCategoryTranslatableContentSerializer(
    serializers.Serializer
):

    language = language = serializers.CharField()
    title = serializers.CharField()
    content = serializers.CharField()


class PartCategoryDataSerializer(
    serializers.Serializer
):

    translatable_content = PartCategoryTranslatableContentSerializer(many=True)


class PartCategorySerializer(
    BaseItemSerializer
):

    item_type = serializers.CharField(default=settings.ITEM_TYPE)
    data = PartCategoryDataSerializer()
