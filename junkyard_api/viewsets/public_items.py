# -*- coding: utf-8 -*-
import datetime

from typing import Final

from django.db.models.query import QuerySet

from rest_framework import mixins, viewsets

from django_filters import rest_framework as filters

from ..filtersets.items import ItemsFilterSet
from ..models import Item
from ..pagination import JunkyardApiPagination
from ..serializers.items import ItemSerializer


class PublicItemsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):

    filter_backends: Final = (filters.DjangoFilterBackend, )
    filterset_class: Final = ItemsFilterSet
    model: Final = Item
    ordering_fields = ['-published_at']
    pagination_class: Final = JunkyardApiPagination
    queryset: Final = model.objects.all()
    serializer_class: Final = ItemSerializer

    def get_queryset(
        self: viewsets.GenericViewSet,
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
