# -*- coding: utf-8 -*-
from junkyard_api.item_types.registry_entry import RegistryEntry

from .conf import settings
from .serializers import PartSerializer


class PartRegistryEntry(RegistryEntry):

    code = settings.ITEM_TYPE
    serializer = PartSerializer
