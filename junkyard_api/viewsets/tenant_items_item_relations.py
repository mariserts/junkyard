# -*- coding: utf-8 -*-
from typing import Final

from rest_framework import mixins, viewsets

from ..models import ItemRelation
from ..pagination import JunkyardApiPagination
from ..permissions import AuthenticatedUserPermission, TenantUserPermission
from ..serializers.item_relations import ItemRelationSerializer


class TenantItemTypeItemsItemRelationsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):

    model: Final = ItemRelation
    ordering_fields: Final = ('id', )
    pagination_class: Final = JunkyardApiPagination
    permission_classes: Final = (
        AuthenticatedUserPermission,
        TenantUserPermission,
    )
    queryset: Final = model.objects.all()
    serializer_class: Final = ItemRelationSerializer
