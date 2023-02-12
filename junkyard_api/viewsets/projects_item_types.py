# -*- coding: utf-8 -*-
from django.db.models.query import QuerySet

from django_filters import rest_framework as filters

from rest_framework import mixins, permissions, viewsets

from ..filtersets.item_types import ItemTypesFilterSet
from ..serializers.item_types import ItemTypeSerializer


class ProjectsItemTypesViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ItemTypesFilterSet
    ordering_fields = ('name', )
    permission_classes = (permissions.IsAuthenticated, )
    queryset = QuerySet()
    serializer_class = ItemTypeSerializer
