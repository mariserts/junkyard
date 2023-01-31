# -*- coding: utf-8 -*-
from typing import Final

from django.db.models import Q
from django.db.models.query import QuerySet

from rest_framework import mixins
from rest_framework.exceptions import ValidationError

from ..filtersets.items import ItemsFilterSet
from ..mixins import ViewSetKwargsMixin, ViewSetPayloadMixin
from ..models import Item
from ..permissions import TenantUserPermission
from ..serializers.items import ItemSerializer

from .base import BaseViewSet


class TenantItemsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    ViewSetKwargsMixin,
    ViewSetPayloadMixin,
    BaseViewSet
):

    filterset_class: Final = ItemsFilterSet
    ordering_fields: Final = ('-id', )
    permission_classes: Final = BaseViewSet.permission_classes + [
        TenantUserPermission, ]
    queryset: Final = Item.objects.all()
    serializer_class: Final = ItemSerializer

    def get_queryset(
        self: BaseViewSet,
    ) -> QuerySet:

        tenant_pk = self.get_kwarg_tenant_pk()
        user_id = self.request.user.id

        queryset = self.queryset.filter(tenant_id=tenant_pk)

        condition = Q()
        condition.add(Q(tenant__owner_id=user_id), Q.OR)
        condition.add(Q(tenant__admins__user_id=user_id), Q.OR)

        queryset = queryset.filter(
            condition
        ).select_related(
            'tenant',
        ).prefetch_related(
            'tenant__admins',
            'parent_items',
        )

        queryset = queryset.order_by(
            *self.ordering_fields
        ).distinct()

        return queryset

    def update(self, request, *args, **kwargs):

        if str(self.get_payload_tenant()) != str(self.get_kwarg_tenant_pk()):
            raise ValidationError({
                'tenant': ['Tenant switching is not allowed']
            })

        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):

        if str(self.get_payload_tenant()) != str(self.get_kwarg_tenant_pk()):
            raise ValidationError({
                'tenant': ['Tenant switching is not allowed']
            })

        return super().create(request, *args, **kwargs)
