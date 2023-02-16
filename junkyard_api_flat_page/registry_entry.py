# -*- coding: utf-8 -*-
from junkyard_api.item_types.registry_entry import RegistryEntry

from .conf import settings
from .filtersets import FlatPageFilterSet
from .serializers import FlatPageSerializer


class FlatPageRegistryEntry(RegistryEntry):

    code = settings.ITEM_TYPE
    filterset = FlatPageFilterSet
    serializer = FlatPageSerializer
