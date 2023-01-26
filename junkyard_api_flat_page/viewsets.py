# -*- coding: utf-8 -*-
from typing import Final

from junkyard_api.viewsets.specific_items import SpecificItemsViewSet

from .conf import settings
from .serializers import FlatPageSerializer


class FlatPageViewSet(SpecificItemsViewSet):

    item_type = settings.ITEM_TYPE
    serializer_class: Final = FlatPageSerializer
