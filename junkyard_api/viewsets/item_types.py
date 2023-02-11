# -*- coding: utf-8 -*-
from typing import List, Type

from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from ..conf import settings
from ..filtersets.item_types import ItemTypesFilterSet
from ..serializers.item_types import ItemTypeSerializer


class ItemTypesViewSet(
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ItemTypesFilterSet
    permission_classes = (permissions.IsAuthenticated, )
    queryset = QuerySet()
    serializer_class = ItemTypeSerializer

    def get_item_types(
        self: Type,
    ) -> List[dict]:

        languages = []

        for name, registry_entry in settings.ITEM_TYPE_REGISTRY.types.items():
            languages.append({
                'name': name
            })

        return languages

    def list(
        self: Type,
        request: Type[Request],
    ) -> Type[Response]:

        languages = self.get_item_types()

        data = {
            'next': None,
            'previous': None,
            'page': 1,
            'pages': 1,
            'total': len(languages),
            'results': self.serializer_class(languages, many=True).data
        }

        return Response(data)
