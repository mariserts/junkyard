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

    def get_types(
        self: BaseItemTypeRegistry,
        root_tenant_only: Union[None, bool] = None,
        format: str = 'list'
    ) -> List[RegistryEntry]:

        types = []

        for key, value in self.types.items():

            add = True

            if root_tenant_only is not None:
                if value.root_tenant_only is not root_tenant_only:
                    add = False

            if add is True:
                types.append(value)

        if format == 'list':
            return types

        output = []

        if format == 'names':
            for item_type in types:
                output.append(item_type.name)

        if format == 'choices':
            for item_type in types:
                output.append([item_type.name, item_type.name])

        return output
