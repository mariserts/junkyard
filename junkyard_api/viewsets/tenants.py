# -*- coding: utf-8 -*-
from typing import Type

from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, viewsets

from ..filtersets.tenants import TenantsFilterSet
from ..models import Tenant, User
from ..pagination import JunkyardApiPagination
from ..serializers.tenants import TenantSerializer


class TenantsViewSet(
    # mixins.CreateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = TenantsFilterSet
    ordering_fields = ('id', )
    pagination_class = JunkyardApiPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    def get_authenticated_queryset(
        self: Type,
    ) -> QuerySet:

        tenant_ids = User.get_tenants(self.request.user, format='ids')

        queryset = self.queryset.filter(
            id__in=tenant_ids,
            is_active=True
        ).order_by(
            *self.ordering_fields
        ).distinct()

        return queryset

    def get_unauthenticated_queryset(
        self: Type,
    ) -> QuerySet:

        queryset = self.queryset.filter(
            is_active=True
        ).order_by(
            *self.ordering_fields
        ).distinct()

        return queryset

    def get_queryset(
        self: Type,
    ) -> QuerySet:

        if self.request.user.is_authenticated is True:
            return self.get_authenticated_queryset()

        return self.get_unauthenticated_queryset()
