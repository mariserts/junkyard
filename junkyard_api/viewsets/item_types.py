# -*- coding: utf-8 -*-
from typing import Final

from django.db.models.query import QuerySet

from rest_framework.request import Request
from rest_framework.response import Response

from ..conf import settings
from ..serializers.item_types import ItemTypeSerializer

from .base import BaseViewSet


class ItemTypesViewSet(
    BaseViewSet
):

    serializer_class: Final = ItemTypeSerializer
    queryset = QuerySet()

    def list(
        self: BaseViewSet,
        request: Request,
    ) -> Response:

        item_types = settings.ITEM_TYPE_REGISTRY.get_types()

        data = {
            'next': None,
            'previous': None,
            'page': 1,
            'pages': 1,
            'total': len(item_types),
            'results': self.serializer_class(item_types, many=True).data
        }

        return Response(data)
