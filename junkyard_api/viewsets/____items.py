# -*- coding: utf-8 -*-
from datetime import datetime, timezone
from typing import Type

from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, viewsets

from ..filtersets.items import ItemsFilterSet
from ..models import Item, User
from ..pagination import JunkyardApiPagination
from ..serializers.items import ItemSerializer


class ItemsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ItemsFilterSet
    ordering_fields = ('-created_at', )
    pagination_class = JunkyardApiPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_authenticated_queryset(
        self: Type,
    ) -> QuerySet:

        tenant_ids = User.get_tenants(self.request.user, format='ids')

        queryset = self.queryset.filter(
            tenant__id__in=tenant_ids,
            tenant__is_active=True,
        ).select_related(
            'tenant'
        ).order_by(
            *self.ordering_fields
        ).distinct()

        return queryset

    def get_unauthenticated_queryset(
        self: Type,
    ) -> QuerySet:

        queryset = self.queryset.filter(
            published=True,
            published_at__lt=datetime.now(timezone.utc),
            tenant__is_active=True,
        ).select_related(
            'tenant'
        ).order_by(
            '-published_at'
        ).distinct()

        return queryset

    def get_queryset(
        self: Type,
    ) -> QuerySet:

        if self.request.user.is_authenticated is True:
            return self.get_authenticated_queryset()

        return self.get_unauthenticated_queryset()
