# -*- coding: utf-8 -*-
from typing import Final

from django.db.models.query import QuerySet

from rest_framework import mixins, viewsets

from django_filters import rest_framework as filters

from ..filtersets.items import ItemsFilterSet
from ..models import Item
from ..pagination import JunkyardApiPagination
from ..serializers.items import ItemSerializer


class SpecificItemsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    item_type = None
    filter_backends: Final = (filters.DjangoFilterBackend, )
    filterset_class: Final = ItemsFilterSet
    model: Final = Item
    ordering_fields = ['-id']
    pagination_class: Final = JunkyardApiPagination
    queryset: Final = model.objects.all()
    serializer_class: Final = ItemSerializer

    def get_queryset(
        self: viewsets.GenericViewSet,
    ) -> QuerySet:

        queryset = self.queryset.filter(
            item_type=self.item_type
        )

        queryset = queryset.filter(
            tenant__owner_id=self.request.user.id
        ).select_related(
            'tenant'
        ).order_by(
            *self.ordering_fields
        )

        return queryset
