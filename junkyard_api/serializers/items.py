# -*- coding: utf-8 -*-
from rest_framework import serializers

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


class DynamicSerializer(ItemSerializer):

    def get_serializer(self, item_type):
        serializer = settings.ITEM_TYPE_REGISTRY.get_serializer(item_type)
        if serializer is None:
            raise serializers.ValidationError({
                'item_type': f'Item type "{item_type}" is not registered'
            })
        return serializer

    def to_representation(self, object):
        try:
            serializer = self.get_serializer(object.item_type)
        except serializers.ValidationError:
            serializer = ItemSerializer
        return serializer(object).data

    def validate(self, data):

        item_type = data['item_type']

        serializer = self.get_serializer(item_type)

        serializer = serializer(data=data)
        if serializer.is_valid() is False:
            raise serializers.ValidationError(serializer.errors)

        return serializer.data

    def create(self, validated_data):
        return Item.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.metadata = validated_data['metadata']
        instance.translatable_content = validated_data['translatable_content']
        instance.published = validated_data['published']
        instance.published_at = validated_data['published_at']
        instance.save()
        return instance

    def validate_tenant(self, value):
        return value.id
