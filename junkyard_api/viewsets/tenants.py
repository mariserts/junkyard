# -*- coding: utf-8 -*-
from typing import Final

from django.db.models import Q
from django.db.models.query import QuerySet

from rest_framework import mixins, viewsets

from django_filters import rest_framework as filters

from ..conf import settings
from ..filtersets.tenants import TenantsFilterSet
from ..models import Tenant
from ..pagination import JunkyardApiPagination
from ..permissions import AuthenticatedUserPermission, TenantUserPermission
from ..serializers.tenants import TenantSerializer


class TenantsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    filter_backends: Final = (filters.DjangoFilterBackend, )
    filterset_class: Final = TenantsFilterSet
    model: Final = Tenant
    ordering_fields: Final = ('id', )
    pagination_class: Final = JunkyardApiPagination
    permission_classes: Final = (
        AuthenticatedUserPermission,
        TenantUserPermission,
    )
    queryset: Final = model.objects.all()
    serializer_class: Final = TenantSerializer

    def get_queryset(
        self: viewsets.GenericViewSet,
    ) -> QuerySet:

        """

        List tenants where user is owner or admin

        Returns:
        - QuerySet of tenants

        """

        user_id = self.request.user.id
        cascade = settings.CASCADE_TENANT_PERMISSIONS

        # Has access to all child tenants if cascade is True

        condition = Q()
        condition.add(Q(owner_id=user_id), Q.OR)
        condition.add(Q(admins__user_id=user_id), Q.OR)

        queryset = self.queryset.filter(
            condition
        ).order_by(
            *self.ordering_fields
        )

        if cascade is False:
            return queryset

        ids = []
        for tenant in queryset:
            ids.append(tenant.id)
            ids += Tenant.get_all_children_ids(tenant)

        ids = list(set(ids))

        return Tenant.objects.filter(
            id__in=ids
        ).order_by(
            *self.ordering_fields
        )
