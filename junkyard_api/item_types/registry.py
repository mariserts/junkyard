# -*- coding: utf-8 -*-
from typing import List

from rest_framework.serializers import Serializer

from ..exceptions import (
    ItemTypeDuplicationException,
    ItemTypeNotFoundException,
)

from .registry_entry import RegistryEntry


class ItemTypeRegistry:

    types = {}

    def register(self, registry_entry: RegistryEntry) -> None:
        if registry_entry.name in self.types:
            raise ItemTypeDuplicationException(
                f'Item type "{registry_entry.name}" already registered'
            )
        self.types[registry_entry.name] = registry_entry

    def find(self, name: str) -> Serializer:
        try:
            return self.types[name]
        except KeyError:
            raise ItemTypeNotFoundException(
                f'Item type "{name}" is not registered'
            )

    def get_serializer(self, name):
        try:
            entry = self.find(name)
        except ItemTypeNotFoundException:
            return None
        return entry.serializer

    def get_viewset(self, name):
        try:
            entry = self.find(name)
        except ItemTypeNotFoundException:
            return None
        return entry.viewset

    def get_type_names_as_choices(self) -> List[List[str]]:
        types = []
        for key in self.types.keys():
            types.append([key, key])
        return types

    def get_type_names_as_list(self) -> List[str]:
        return list(self.types.keys())

    def get_types_as_list(self) -> List[RegistryEntry]:
        types = []
        for key, value in self.types.items():
            types.append(value)
        return types
