# -*- coding: utf-8 -*-
from typing import Final

from django.db.models.query import QuerySet

from rest_framework import mixins, viewsets

from ..mixins import ViewSetKwargsMixin
from ..models import ItemRelation
from ..pagination import JunkyardApiPagination
from ..permissions import (
    AuthenticatedUserPermission,
    TenantUserPermission,
)
from ..serializers.item_relations import ItemRelationSerializer


class TenantItemItemRelationsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    ViewSetKwargsMixin,
    viewsets.GenericViewSet
):

    model: Final = ItemRelation
    ordering_fields: Final = ('id', )
    pagination_class: Final = JunkyardApiPagination
    permission_classes: Final = [
        AuthenticatedUserPermission,
        TenantUserPermission,
    ]
    queryset: Final = model.objects.all()
    serializer_class: Final = ItemRelationSerializer

    def get_queryset(
        self: viewsets.GenericViewSet,
    ) -> QuerySet:

        tenant_pk = self.get_kwarg_tenant_pk()
        item_pk = self.get_kwarg_item_pk()

        queryset = self.queryset.filter(
            child_id=item_pk,
            child__tenant_id=tenant_pk,
        ).select_related(
            'child'
        ).order_by(
            *self.ordering_fields
        )

        return queryset
