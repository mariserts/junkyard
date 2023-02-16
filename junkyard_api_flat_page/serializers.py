# -*- coding: utf-8 -*-
from rest_framework import serializers

from junkyard_api.serializers.items import BaseItemSerializer

from .conf import settings


class FlatPageTranslatableContentSerializer(
    serializers.Serializer
):

    language = serializers.CharField()
    title = serializers.CharField()
    slug = serializers.SlugField()
    content = serializers.CharField()


class FlatPageDataSerializer(
    serializers.Serializer
):

    translatable_content = FlatPageTranslatableContentSerializer(many=True)


class FlatPageSerializer(
    BaseItemSerializer
):

    item_type = serializers.CharField(default=settings.ITEM_TYPE)
    data = FlatPageDataSerializer()
