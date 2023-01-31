# -*- coding: utf-8 -*-
from typing import Final

from django.db.models.query import QuerySet

from rest_framework import mixins, serializers

from ..mixins import ViewSetKwargsMixin
from ..models import ItemRelation
from ..permissions import TenantUserPermission
from ..serializers.item_relations import ItemRelationSerializer

from .base import BaseViewSet


class TenantItemItemRelationsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    ViewSetKwargsMixin,
    BaseViewSet
):

    ordering_fields: Final = ('id', )
    permission_classes: Final = BaseViewSet.permission_classes + [
        TenantUserPermission, ]
    queryset: Final = ItemRelation.objects.all()
    serializer_class: Final = ItemRelationSerializer

    def get_queryset(
        self: BaseViewSet,
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

    def create(self, request, *args, **kwargs):

        item_pk = self.get_kwarg_item_pk()
        child = request.data.get('child', item_pk)

        if str(item_pk) != str(child):
            raise serializers.ValidationError({
                'child': ['Child item switching is not allowed']
            })

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):

        item_pk = self.get_kwarg_item_pk()
        child = request.data.get('child', item_pk)

        if str(item_pk) != str(child):
            raise serializers.ValidationError({
                'child': ['Child item switching is not allowed']
            })

        return super().update(request, *args, **kwargs)
