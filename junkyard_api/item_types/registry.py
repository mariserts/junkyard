# -*- coding: utf-8 -*-
from typing import List, Union

from rest_framework.serializers import Serializer

from ..exceptions import (
    ItemTypeDuplicationException,
    ItemTypeNotFoundException,
)

from .registry_entry import RegistryEntry


class BaseItemTypeRegistry:
    pass


class ItemTypeRegistry(BaseItemTypeRegistry):

    types = {}

    def register(
        self: BaseItemTypeRegistry,
        registry_entry: RegistryEntry
    ) -> None:
        if registry_entry.name in self.types:
            raise ItemTypeDuplicationException(
                f'Item type "{registry_entry.name}" already registered'
            )
        self.types[registry_entry.name] = registry_entry

    def find(
        self: BaseItemTypeRegistry,
        name: str
    ) -> Serializer:
        try:
            return self.types[name]
        except KeyError:
            raise ItemTypeNotFoundException(
                f'Item type "{name}" is not registered'
            )

    def get_serializer(
        self: BaseItemTypeRegistry,
        name: str
    ) -> Union[None, Serializer]:
        try:
            entry = self.find(name)
        except ItemTypeNotFoundException:
            return None
        return entry.serializer

    def get_type_names_as_choices(
        self: BaseItemTypeRegistry,
        root_tenant_only: Union[None, bool] = None,
    ) -> List[List[str]]:

        output = []

        item_types = self.get_types_as_list(
            root_tenant_only=root_tenant_only
        )

        for item_type in item_types:
            output.append([item_type.name, item_type.name])

        return output

    def get_type_names_as_list(
        self: BaseItemTypeRegistry,
        root_tenant_only: Union[None, bool] = None,
    ) -> List[str]:

        output = []

        item_types = self.get_types_as_list(
            root_tenant_only=root_tenant_only
        )

        for item_type in item_types:
            output.append(item_type.name)

        return output

    def get_types_as_list(
        self: BaseItemTypeRegistry,
        root_tenant_only: Union[None, bool] = None,
    ) -> List[RegistryEntry]:

        types = []

        for key, value in self.types.items():

            add = True

            if root_tenant_only is not None:
                if value.root_tenant_only is root_tenant_only:
                    add = False

            if add is True:
                types.append(value)

        return types
