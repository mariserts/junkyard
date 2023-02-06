# -*- coding: utf-8 -*-
from typing import Final

from django.db.models.query import QuerySet

from rest_framework import mixins

from ..filtersets.items import ItemsFilterSet
from ..models import Item, User
from ..serializers.items import ItemSerializer

from .base import BaseViewSet


class ItemsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    BaseViewSet
):

    filterset_class: Final = ItemsFilterSet
    ordering_fields = ['-created_at']
    queryset: Final = Item.objects.all()
    serializer_class: Final = ItemSerializer

    def get_queryset(
        self: BaseViewSet,
    ) -> QuerySet:

        # Get all tenant ids for user
        tenant_ids = User.get_tenants(self.request.user, format='ids')

        # Tenant is active
        queryset = self.queryset.filter(
            tenant__id__in=tenant_ids,
            tenant__is_active=True,
        ).select_related(
            'tenant'
        ).order_by(
            *self.ordering_fields
        )

        return queryset
