# -*- coding: utf-8 -*-
from typing import List, Tuple, Union

from rest_framework import serializers

from ..conf import settings
from ..exceptions import ItemTypeNotFoundException
from ..models import Item, ItemRelation, SearchVector, Tenant, User

from .item_relations import NestedItemRelationSerializer
from .mixins import ItemShortcutsMixin


class ItemSerializer(
    ItemShortcutsMixin,
    serializers.ModelSerializer
):

    _existing_relations_ids = []
    _createble_relations = []

    id = serializers.IntegerField(required=False)
    item_type = serializers.ChoiceField(choices=())
    metadata = serializers.JSONField(default=dict, required=False)
    translatable_content = serializers.JSONField(default=[], required=False)
    published = serializers.BooleanField(default=False)
    published_at = serializers.DateTimeField(required=False)
    parent_items = NestedItemRelationSerializer(many=True, required=False)

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
        field.choices = settings.ITEM_TYPE_REGISTRY.get_types(format='choices')

    #
    # Representation
    #

    def to_representation(
        self: serializers.BaseSerializer,
        object: Union[Item, List[Item]],
    ) -> Union[List, dict]:

        if self.context.get('_nested', True) is True:

            output = []

            many = True
            instances = object

            if type(object) != list:
                many = False
                instances = [object, ]

            for instance in instances:

                item_type = instance.item_type
                serializer = settings.ITEM_TYPE_REGISTRY.get_serializer(
                    item_type)
                if serializer is None:
                    serializer = ItemSerializer

                context = self.context.copy()
                context['_nested'] = False

                # XXXX perf issues: Doubles amount of validation?
                output_data = serializer(instance, context=context).data

                output.append(output_data)

            if many is True:
                return output

            return next(iter(output), None)

        return super().to_representation(object)

    #
    # Field validation
    #

    def validate_item_type(self, value):

        # Item type can not be changed if item is being updated

        if self.instance is not None:
            return self.instance_item_type

        # Check item type when creating item

        if self.instance is not None:
            tenant_pk = self.instance_item_type
        else:
            tenant_pk = self.raw_tenant_pk

        is_root = Tenant.is_root_tenant(tenant_pk)

        try:
            item_type = settings.ITEM_TYPE_REGISTRY.find(value)
        except ItemTypeNotFoundException:
            raise serializers.ValidationError(
                'Item type does not exist'
            )

        if item_type.root_tenant_only is not is_root:
            raise serializers.ValidationError(
                'Tenant has no access to this item type'
            )

        return item_type.name

    def validate_tenant(self, value):

        # Tenant can not be changed if item is updated

        if self.instance is not None:
            return self.instance.tenant

        # Check tenant when creating item

        if self.request_user is None:
            raise serializers.ValidationError('No request user found')

        tenant_ids = User.get_tenants(self.request_user, format='ids')

        if value.id not in tenant_ids:
            raise serializers.ValidationError(
                f'User has no access to tenant "{value}"'
            )

        return value

    #
    # Save
    #

    def save(
        self: serializers.BaseSerializer,
        **kwargs: dict
    ) -> Item:

        self.pre_save()

        validated_data = {**self.validated_data, **kwargs}

        self.set_parent_items_management_data(self.instance, validated_data)

        #
        if 'parent_items' in self.validated_data:
            del self.validated_data['parent_items']

        #
        instance = super().save(**kwargs)

        self.manage_parent_items_relations(instance, validated_data)

        self.post_save(instance, validated_data)
        self.manage_search_vectors(instance)

        return instance

    #
    # Pre save actions
    #

    def pre_save(
        self: serializers.BaseSerializer,
    ) -> None:

        """

        Pre save actions to do

        Returns:
        - None

        """

        pass

    #
    # Post save actions
    #

    def set_parent_items_management_data(
        self: serializers.BaseSerializer,
        instance: Item,
        validated_data: dict,
    ) -> None:

        """

        Sets data for item relation management

        Attrs:
        - instance Item: - item object
        - validated_data dict: - serializer validated data

        Returns:
        - None

        """

        parent_items = validated_data.get('parent_items', [])
        instance_id = getattr(instance, 'id', None)

        errors = {'parent_items': []}
        self._parent_items_to_create = []
        self._parent_items_to_update = []
        self._parent_items_to_update_ids = []
        self._parent_items_ids_to_delete = []
        self._parent_items_existing_relations_ids = []

        #
        if instance is not None:
            self._parent_items_existing_relations_ids = list(
                instance.parent_items.all().values_list('id', flat=True)
            )

        #
        for parent_item in parent_items:

            child_id = parent_item.get('child_id', None)
            id = parent_item.get('id', None)
            create = id is None

            if instance_id != child_id:
                errors['parent_items'].append({
                    'child': 'Child id must match instance id'
                })
            else:
                if create is True:
                    self._parent_items_to_create.append(parent_item)
                else:
                    self._parent_items_to_update_ids.append(id)
                    self._parent_items_to_update.append(parent_item)

        #
        if len(errors['parent_items']) > 0:
            raise serializers.ValidationError(errors)

        #
        if len(self._parent_items_existing_relations_ids) > 0:
            self._parent_items_ids_to_delete = list(
                set(self._parent_items_existing_relations_ids).difference(
                    set(self._parent_items_to_update_ids)
                )
            )

    def manage_parent_items_relations(
        self: serializers.BaseSerializer,
        instance: Item,
        validated_data: dict,
    ) -> None:

        """

        Manages item relation management

        Attrs:
        - instance Item: - saved item object
        - validated_data dict: - serializer validated data

        Returns:
        - None

        """

        #
        if len(self._parent_items_ids_to_delete) > 0:
            ItemRelation.objects.filter(
                id__in=self._parent_items_ids_to_delete
            ).delete()

        #
        for parent_item in self._parent_items_to_create:
            parent_item['child'] = instance
            ItemRelation.objects.create(**parent_item)

        #
        for parent_item in self._parent_items_to_update:
            parent_item['child'] = instance
            ItemRelation.objects.filter(
                id=parent_item['id']
            ).update(
                **parent_item
            )

    def post_save(
        self: serializers.BaseSerializer,
        instance: Item,
        initial_validated_data: dict,
    ) -> None:

        """

        Post save actions to do

        Attrs:
        - instance Item: item object
        - initial_validated_data: initial validated data before save is called

        Returns:
        - None

        """

        pass

    @staticmethod
    def create_search_vectors(
        instance: Item,
    ) -> None:

        """

        Method to create search vectors
        Called after item save in manage_search_vectors
        Make metadata and translatable_content data more accessible

        Attrs:
        - instance Item: item object

        Returns:
        - None

        """

    def manage_search_vectors(
        self: serializers.BaseSerializer,
        instance: Item,
    ) -> None:

        """

        Entrypoint for search vector management logic

        Attrs:
        - instance Item: item object

        Returns:
        - None

        """

        SearchVector.objects.filter(
            item_id=instance.id
        ).delete()

        item_type = instance.item_type
        serializer = settings.ITEM_TYPE_REGISTRY.get_serializer(item_type)
        if serializer is not None:
            serializer = serializer.create_search_vectors(instance)
