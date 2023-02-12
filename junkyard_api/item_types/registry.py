# -*- coding: utf-8 -*-
from collections import OrderedDict
from typing import List, Type, Union

from rest_framework.serializers import Serializer

from ..exceptions import (
    ItemTypeDuplicationException,
    ItemTypeNotFoundException,
)

from .registry_entry import RegistryEntry


class ItemTypeRegistry:

    types = OrderedDict()

    def register(
        self: Type,
        registry_entry: Type[RegistryEntry]
    ) -> None:
        if registry_entry.name in self.types:
            raise ItemTypeDuplicationException(
                f'Item type "{registry_entry.name}" already registered'
            )
        self.types[registry_entry.name] = registry_entry

    def find(
        self: Type,
        name: str
    ) -> Type[RegistryEntry]:
        try:
            return self.types[name]
        except KeyError:
            raise ItemTypeNotFoundException(
                f'Item type "{name}" is not registered'
            )

    def get_serializer(
        self: Type,
        name: str
    ) -> Union[None, Type[Serializer]]:
        try:
            entry = self.find(name)
        except ItemTypeNotFoundException:
            return None
        return entry.serializer

    def get_types(
        self: Type,
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
