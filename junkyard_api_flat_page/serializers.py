# -*- coding: utf-8 -*-
from rest_framework import serializers

from junkyard_api.models import Item, SearchVector
from junkyard_api.serializers.items import ItemSerializer

from .conf import settings


class FlatPageTranslatableContentSerializer(serializers.Serializer):

    language = serializers.ChoiceField(
        choices=[],
        default=''
    )
    title = serializers.CharField()
    slug = serializers.SlugField()
    content = serializers.CharField()


class FlatPageSerializer(ItemSerializer):

    item_type = serializers.CharField(default=settings.ITEM_TYPE)
    translatable_content = FlatPageTranslatableContentSerializer(many=True)

    def __init__(self, *args, **kwargs):
        super(serializers.ModelSerializer, self).__init__(*args, **kwargs)

    @staticmethod
    def create_search_vectors(
        instance: Item,
    ) -> None:

        for content in instance.translatable_content:

            language = content.get('language', None)

            if language is not None:

                SearchVector.objects.create(
                    field_name='translatable_content__title',
                    item=instance,
                    language=language,
                    raw_value=content['title'],
                    vector=content['title'],
                )
