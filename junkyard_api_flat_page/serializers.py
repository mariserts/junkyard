# -*- coding: utf-8 -*-
from rest_framework import serializers

from junkyard_api.conf import settings as junkyard_api_settings
from junkyard_api.models import Item
from junkyard_api.serializers.items import ItemSerializer

from .conf import settings


class FlatPageTranslatableContentSerializer(serializers.Serializer):

    language = serializers.ChoiceField(
        choices=junkyard_api_settings.LANGUAGES,
        default=junkyard_api_settings.LANGUAGE_DEFAULT
    )
    title = serializers.CharField()
    content = serializers.CharField()


class FlatPageSerializer(ItemSerializer):

    translatable_content = FlatPageTranslatableContentSerializer(many=True)
