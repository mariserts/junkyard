# -*- coding: utf-8 -*-
from typing import Type

from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from ..conf import settings
from ..filtersets.item_types import ItemTypesFilterSet
from ..models import Tenant
from ..serializers.item_types import ItemTypeSerializer


class ItemTypesViewSet(
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ItemTypesFilterSet
    ordering_fields = ('-created_at', )
    permission_classes = (permissions.AllowAny, )
    queryset = QuerySet()
    serializer_class = ItemTypeSerializer

    def list(
        self: Type,
        request: Request,
    ) -> Response:

        is_root = None

        tenant_pk = request.GET.get('tenant', None)
        if tenant_pk is not None:
            tenant = Tenant.objects.filter(pk=tenant_pk).first()
            if tenant is not None:
                is_root = tenant.parent is None

        item_types = settings.ITEM_TYPE_REGISTRY.get_types(
            root_tenant_only=is_root,
            format='list'
        )

        data = {
            'next': None,
            'previous': None,
            'page': 1,
            'pages': 1,
            'total': len(item_types),
            'results': self.serializer_class(item_types, many=True).data
        }

        return Response(data)
