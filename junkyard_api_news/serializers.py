# -*- coding: utf-8 -*-
from rest_framework import serializers

from junkyard_api.conf import settings as junkyard_api_settings
from junkyard_api.serializers.items import ItemSerializer

from .conf import settings


class NewsTranslatableContentSerializer(serializers.Serializer):

    language = serializers.ChoiceField(
        choices=junkyard_api_settings.LANGUAGES,
        default=junkyard_api_settings.LANGUAGE_DEFAULT
    )
    title = serializers.CharField()
    slug = serializers.SlugField(required=False)
    content = serializers.CharField()


class NewsSerializer(ItemSerializer):

    item_type = serializers.CharField(default=settings.ITEM_TYPE)
    translatable_content = NewsTranslatableContentSerializer(many=True)

    def __init__(self, *args, **kwargs):
        super(serializers.ModelSerializer, self).__init__(*args, **kwargs)
