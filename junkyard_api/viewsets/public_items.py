# -*- coding: utf-8 -*-
import datetime

from typing import Final

from django.db.models.query import QuerySet

from rest_framework import mixins

from ..filtersets.items import ItemsFilterSet
from ..models import Item
from ..permissions import ReadOnlyPermission
from ..serializers.items import ItemSerializer

from .base import BaseViewSet


class PublicItemsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    BaseViewSet
):

    filterset_class: Final = ItemsFilterSet
    ordering_fields = ['-published_at']
    permission_classes = [ReadOnlyPermission, ]
    queryset: Final = Item.objects.all()
    serializer_class: Final = ItemSerializer

    def get_queryset(
        self: BaseViewSet,
    ) -> QuerySet:

        # Item is published
        queryset = self.queryset.filter(
            published=True,
            published_at__lt=datetime.datetime.now(datetime.timezone.utc),
        )

        # Tenant is active
        queryset = queryset.filter(
            tenant__is_active=True,
        ).select_related(
            'tenant'
        ).order_by(
            *self.ordering_fields
        )

        return queryset
