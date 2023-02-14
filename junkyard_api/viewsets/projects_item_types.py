# -*- coding: utf-8 -*-
from typing import Type

from django.db.models.query import QuerySet

from django_filters import rest_framework as filters

from rest_framework import mixins, permissions, viewsets

from ..filtersets.projects_item_types import ProjectsItemTypesFilterSet
from ..models import ItemType
from ..pagination import JunkyardApiPagination
from ..serializers.item_types import ItemTypeSerializer


class ProjectsItemTypesViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProjectsItemTypesFilterSet
    ordering_fields = ('code', )
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
