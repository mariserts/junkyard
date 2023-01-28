# -*- coding: utf-8 -*-
from typing import List, Tuple, Union

from rest_framework import serializers
from rest_framework.reverse import reverse

from drf_writable_nested.serializers import WritableNestedModelSerializer

from ..conf import settings
from ..models import Item, ItemRelation
from ..serializers.item_relations import ItemRelationSerializer


class ItemSerializer(WritableNestedModelSerializer):

    item_type = serializers.ChoiceField(choices=())
    metadata = serializers.JSONField(default=dict, required=False)
    translatable_content = serializers.JSONField(default=[], required=False)
    published = serializers.BooleanField(default=False)
    published_at = serializers.DateTimeField(required=False)
    parent_items = ItemRelationSerializer(many=True, required=False)

    class Meta:
        model = Item
        fields = '__all__'

    def __init__(
        self: serializers.BaseSerializer,
        *args: Union[List, Tuple],
        **kwargs: dict
    ) -> None:

        super(ItemSerializer, self).__init__(*args, **kwargs)

        field = self.fields['item_type']
        field.choices = settings.ITEM_TYPE_REGISTRY.get_type_names_as_choices()

    def save(
        self: serializers.BaseSerializer,
        **kwargs: dict
    ) -> Item:

        validated_data = {**self.validated_data, **kwargs}
        parent_items = validated_data.get('parent_items', [])
        relations_to_delete = []

        if self.instance is not None:
            if len(parent_items) == 0:
                relations_to_delete = list(
                    self.instance.parent_items.all().values_list(
                        'id',
                        flat=True
                    )
                )

        instance = super().save(**kwargs)

        if len(relations_to_delete) > 0:
            ItemRelation.objects.filter(
                id__in=relations_to_delete
            ).delete()

        return instance


class DynamicReadOnlySerializer(serializers.Serializer):

    def get_dynamic_serializer(
        self: serializers.BaseSerializer,
        item_type: str
    ) -> serializers.Serializer:

        serializer = settings.ITEM_TYPE_REGISTRY.get_serializer(item_type)
        if serializer is None:
            return ItemSerializer

        return serializer

    def to_representation(
        self: serializers.BaseSerializer,
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
                'items-detail',
                args=[object.tenant_id, object.id],
                request=self.context.get('request', None)
            )

            output.append(data)

        if many is True:
            return output

        return next(iter(output), None)
