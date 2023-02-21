# -*- coding: utf-8 -*-
from typing import Type

from django.db.models.query import QuerySet

from rest_framework import permissions, mixins, viewsets

from django_filters import rest_framework as filters

from ..filtersets.item_types import ItemTypesFilterSet
from ..models import ItemType
from ..pagination import JunkyardApiPagination
from ..serializers.item_types import ItemTypeSerializer


class ItemTypesViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ItemTypesFilterSet
    ordering_fields = ['code', ]
    pagination_class = JunkyardApiPagination
    permission_classes = (permissions.IsAuthenticated, )
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer

    def get_queryset(
        self: Type,
    ) -> QuerySet:

        return self.queryset.order_by(
            *self.ordering_fields
        )
