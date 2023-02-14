# -*- coding: utf-8 -*-
from rest_framework import serializers

from junkyard_api.serializers.items import BaseItemSerializer

from .conf import settings


class NewsTranslatableContentSerializer(
    serializers.Serializer
):

    language = language = serializers.CharField()
    title = serializers.CharField()
    slug = serializers.SlugField(required=False)
    content = serializers.CharField()


class NewsSerializer(
    BaseItemSerializer
):

    item_type = serializers.CharField(default=settings.ITEM_TYPE)
    translatable_content = NewsTranslatableContentSerializer(many=True)
