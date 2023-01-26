# -*- coding: utf-8 -*-
from typing import List, Union

from rest_framework import serializers
from rest_framework.reverse import reverse

from ..conf import settings
from ..models import Item


class ItemSerializer(serializers.ModelSerializer):

    item_type = serializers.ChoiceField(choices=())
    metadata = serializers.JSONField(default=dict, required=False)
    translatable_content = serializers.JSONField(default=[], required=False)
    published = serializers.BooleanField(default=False)
    published_at = serializers.DateTimeField(required=False)

    class Meta:
        model = Item
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super(ItemSerializer, self).__init__(*args, **kwargs)

        field = self.fields['item_type']
        field.choices = settings.ITEM_TYPE_REGISTRY.get_type_names_as_choices()

    def get_display_content(
        self,
        fallback_language: str = settings.LANGUAGE_DEFAULT,
        language: str = settings.LANGUAGE_DEFAULT
    ) -> dict:

        language_content = None
        fallback_content = None

        for translatable_content in self.translatable_content:

            _language = translatable_content.get('language', '-1')

            if _language == fallback_language:
                fallback_content = translatable_content.copy()
            if _language == language:
                fallback_content = translatable_content.copy()

        if language_content is not None:
            return language_content

        return fallback_content


class DynamicReadOnlySerializer(serializers.Serializer):

    def get_dynamic_serializer(
        self: serializers.ModelSerializer,
        item_type: str
    ) -> serializers.Serializer:

        serializer = settings.ITEM_TYPE_REGISTRY.get_serializer(item_type)
        if serializer is None:
            return ItemSerializer

        return serializer

    def to_representation(
        self: serializers.Serializer,
        instance: Union[Item, List[Item]]
    ) -> dict:

        many = False
        if type(instance) == list:
            many = True

        if many is False:
            instance = [instance, ]

        output = []

        for object in instance:

            serializer = self.get_dynamic_serializer(object.item_type)

            data = serializer(object, context=self.context).data

            data['link'] = reverse(
                f'{object.item_type}-items-detail',
                args=[object.tenant_id, object.id],
                request=self.context.get('request', None)
            )

            output.append(data)

        if many is True:
            return output

        return next(iter(output), None)
