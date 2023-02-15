# -*- coding: utf-8 -*-
from typing import List, Type, Union

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..conf import settings
from ..models import Item, ItemType, ItemRelation


class BaseItemRelationSerializer(serializers.Serializer):

    id = serializers.IntegerField(
        allow_null=True, required=False, read_only=True)
    parent = serializers.IntegerField()
    child = serializers.IntegerField(allow_null=True, required=False)
    label = serializers.CharField()
    metadata = serializers.JSONField(default=dict, required=False)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class BaseItemSerializer(serializers.Serializer):

    id = serializers.IntegerField(
        allow_null=True, required=False, read_only=True)

    project = serializers.IntegerField()
    tenant = serializers.IntegerField(allow_null=True, required=False)
    moved_to = serializers.IntegerField(allow_null=True, required=False)
    item_type = serializers.CharField()

    metadata = serializers.JSONField(default=dict, required=False)
    translatable_content = serializers.JSONField(default=list, required=False)

    parent_items = BaseItemRelationSerializer(many=True, required=False)

    archived = serializers.BooleanField(default=False)
    archived_at = serializers.DateTimeField(required=False, allow_null=True)
    published = serializers.BooleanField(default=False)
    published_at = serializers.DateTimeField(required=False, allow_null=True)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    @staticmethod
    def pre_save(
        instance: Type,
        validated_data: dict
    ) -> None:
        return None

    @staticmethod
    def post_save(
        instance: Type,
        validated_data: dict
    ) -> None:
        return None


class BaseItemModelSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Item
        fields = '__all__'


class ItemSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Item
        exclude = [
            'moved_to',
            'project',
            'tenant',
        ]

    project_id = serializers.IntegerField()
    tenant_id = serializers.IntegerField(required=False, allow_null=True)
    moved_to_id = serializers.IntegerField(required=False, allow_null=True)

    archived = serializers.BooleanField(default=False)
    archived_at = serializers.DateTimeField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    published = serializers.BooleanField(default=False)
    published_at = serializers.DateTimeField(required=False, allow_null=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def to_representation(
        self: Type,
        object: Type[Item],
    ) -> dict:
        data = BaseItemModelSerializer(object).data
        data['item_type'] = object.item_type.code
        return data

    def run_validation_parent_items(
        self: Type,
        parent_items: List
    ) -> dict:
        instance_id = getattr(self.instance, 'id', None)

        errors = []
        ids = []
        relations_to_create = []
        relations_to_delete = []
        relations_to_update = []

        for relation in parent_items:

            relation['parent_id'] = relation.get('parent', None)
            relation.pop('parent')

            relation['child_id'] = relation.get('child', None)
            relation.pop('child')

            id = relation.get('id', None)
            child = relation.get('child_id', None)
            parent = relation.get('parent_id', None)

            if parent is None:
                break

            if id is not None and instance_id is not None:
                if child == instance_id:
                    relations_to_update.append(relation)
                    ids.append(ids)
                else:
                    errors.append(
                        'Can not update parent relations for other items')

            if id is None:
                if child == instance_id:
                    relations_to_create.append(relation)
                else:
                    errors.append(
                        'Can not create parent relations for other items')

        if len(errors) != 0:
            raise ValidationError(detail=str(errors))

        if self.instance is not None:
            if self.context['request'].method.upper() == 'PUT':
                relations_to_delete = list(
                    self.instance.parents.all().exclude(
                        id__in=ids
                    )
                )

        data = {
            'create': relations_to_create,
            'delete': relations_to_delete,
            'update': relations_to_update,
        }

        return data

    def run_validation(
        self: Type,
        data: dict
    ) -> dict:

        _data = data.copy()

        registry_entry = self.get_registry_entry(str(_data['item_type']))

        validated_data = registry_entry.serializer().run_validation(data)

        item_type_code = validated_data.get('item_type', None)
        moved_to_id = validated_data.get('moved_to', None)
        project_id = validated_data.get('project', None)
        tenant_id = validated_data.get('tenant', None)
        parent_items = validated_data.get('parent_items', [])

        validated_data.pop('moved_to', None)
        validated_data.pop('project', None)
        validated_data.pop('tenant', None)
        validated_data.pop('parent_items', None)

        # Remap fields

        validated_data['item_type'] = ItemType.objects.get(code=item_type_code)
        validated_data['moved_to_id'] = moved_to_id
        validated_data['project_id'] = project_id
        validated_data['tenant_id'] = tenant_id
        self._parent_items_set = self.run_validation_parent_items(parent_items)

        return validated_data

    def write_parent_relation_relations(
        self: Type,
        instance: Union[Type[Item], None]
    ):

        relation_set = getattr(self, '_parent_items_set', {})

        create = relation_set.get('create', [])
        delete = relation_set.get('delete', [])
        update = relation_set.get('update', [])

        for relation in delete:
            relation.delete()

        for relation in create:
            relation['child_id'] = instance.id
            ItemRelation.objects.create(**relation)

        for relation in update:
            ItemRelation.objects.filter(
                id=relation['id'],
                child_id=instance.id
            ).update(
                parent_id=relation['parent_id'],
                label=relation.get('label', {}),
                metadata=relation.get('metadata', {}),
            )

    def save(
        self: Type,
        **kwargs: dict
    ) -> Item:

        validated_data = {
            **self.validated_data, **kwargs
        }

        registry_entry = self.get_registry_entry(
            validated_data['item_type'].code
        )

        registry_entry.serializer.pre_save(
            self.instance,
            validated_data
        )

        instance = super().save(**kwargs)

        self.write_parent_relation_relations(instance)

        registry_entry.serializer.post_save(
            instance,
            validated_data
        )

        return instance

    def get_registry_entry(self, item_type):
        registry_entry = settings.ITEM_TYPE_REGISTRY.get_type(item_type)
        if registry_entry is None:
            raise ValidationError(detail=f'Item type "{item_type}" not found')
        return registry_entry
