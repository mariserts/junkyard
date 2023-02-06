# -*- coding: utf-8 -*-
from typing import Type

from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, viewsets

from ..filtersets.admins import AdminsFilterSet
from ..models import TenantAdmin, User
from ..pagination import JunkyardApiPagination
from ..serializers.admins import AdminSerializer


class AdminsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = AdminsFilterSet
    ordering_fields = ('-id', )
    pagination_class = JunkyardApiPagination
    permission_classes = (permissions.IsAuthenticated, )
    queryset = TenantAdmin.objects.all()
    serializer_class = AdminSerializer

    def get_queryset(
        self: Type,
    ) -> QuerySet:

        tenant_ids = User.get_tenants(self.request.user, format='ids')

        queryset = self.queryset.filter(
            tenant_id__in=tenant_ids
        ).order_by(
            *self.ordering_fields
        ).distinct()

        return queryset
