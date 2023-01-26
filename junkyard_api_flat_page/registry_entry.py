# -*- coding: utf-8 -*-
from junkyard_api.item_types.registry_entry import RegistryEntry

from .conf import settings
from .serializers import FlatPageSerializer
from .viewsets import FlatPageViewSet


class FlatPageRegistryEntry(RegistryEntry):

    name = settings.ITEM_TYPE
    serializer = FlatPageSerializer
    viewset = FlatPageViewSet
