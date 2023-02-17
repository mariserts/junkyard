# -*- coding: utf-8 -*-
from collections import OrderedDict
from typing import List, Type, Union

from django.db import connection

from ..models import ItemType

from ..exceptions import ItemTypeDuplicationException

from .registry_entry import RegistryEntry


class ItemTypeRegistry:

    types = OrderedDict()

    def sync_db(
        self: Type
    ) -> None:

        table_names = connection.introspection.table_names()
        if 'junkyard_api_itemtype' not in table_names:
            return None

        codes = list(self.types.keys())

        for code in codes:

            item_type = ItemType.objects.filter(code=code).first()

            if item_type is None:
                ItemType.objects.create(
                    code=code,
                    is_active=True,
                )

            else:
                item_type.is_active = True
                item_type.save()

        ItemType.objects.all().exclude(
            code__in=codes
        ).update(
            is_active=False
        )

    def register(
        self: Type,
        registry_entry: Type[RegistryEntry]
    ) -> None:

        if registry_entry.code in self.types:
            raise ItemTypeDuplicationException(
                f'Item type "{registry_entry.code}" already registered'
            )

        self.types[registry_entry.code] = registry_entry

    def get_type(
        self: Type,
        code: str,
    ) -> Union[Type[RegistryEntry], None]:

        return self.types.get(code, None)

    def get_types(
        self: Type,
    ) -> List[RegistryEntry]:

        return self.types
