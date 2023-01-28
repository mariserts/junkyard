# -*- coding: utf-8 -*-
from typing import Final

from django.db.models import Q
from django.db.models.query import QuerySet

from rest_framework import mixins, viewsets
from rest_framework.exceptions import ValidationError

from django_filters import rest_framework as filters

from ..filtersets.items import ItemsFilterSet
from ..models import Item
from ..pagination import JunkyardApiPagination
from ..permissions import (
    AuthenticatedUserPermission,
    TenantUserPermission,
)
from ..serializers.items import ItemSerializer


class TenantItemsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    filter_backends: Final = (filters.DjangoFilterBackend, )
    filterset_class: Final = ItemsFilterSet
    model: Final = Item
    ordering_fields: Final = ('-id', )
    pagination_class: Final = JunkyardApiPagination
    permission_classes: Final = [
        AuthenticatedUserPermission,
        TenantUserPermission,
    ]
    queryset: Final = model.objects.all()
    serializer_class: Final = ItemSerializer

    def get_payload_tenant(
        self: viewsets.GenericViewSet,
    ) -> int:
        return self.request.data['tenant']

    def get_kwarg_tenant_pk(
        self: viewsets.GenericViewSet
    ) -> str:
        return self.kwargs['tenant_pk']

    def get_queryset(
        self: viewsets.GenericViewSet,
    ) -> QuerySet:

        tenant_pk = self.kwargs.get('tenant_pk', None)
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
            'tenant__admins'
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
