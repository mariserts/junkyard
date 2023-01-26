# -*- coding: utf-8 -*-
from typing import Final

from junkyard_api.viewsets.tenant_item_type_items import (
    TenantItemTypeItemsViewSet
)

from .conf import settings
from .serializers import FlatPageSerializer


class TenantFlatPageViewSet(TenantItemTypeItemsViewSet):

    item_type: Final = settings.ITEM_TYPE
    serializer_class: Final = FlatPageSerializer
