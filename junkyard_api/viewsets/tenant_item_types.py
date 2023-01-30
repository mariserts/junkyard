# -*- coding: utf-8 -*-
from typing import Final, Union

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from ..mixins import ViewSetKwargsMixin
from ..permissions import AuthenticatedUserPermission, TenantUserPermission
from ..serializers.item_types import ItemTypeSerializer


class TenantItemTypesViewSet(
    ViewSetKwargsMixin,
    viewsets.GenericViewSet
):

    permission_classes: Final = (
        AuthenticatedUserPermission,
        TenantUserPermission,
    )
    serializer_class: Final = ItemTypeSerializer

    def list(
        self: viewsets.GenericViewSet,
        request: Request,
        tenant_pk: int
    ) -> Response:

        return Response({
            'next': None,
            'previous': None,
            'page': 1,
            'pages': 1,
            'total': 0
        })

    def get(
        self: viewsets.GenericViewSet,
        request: Request,
        tenant_pk: int,
        pk: Union[None, int]
    ) -> Response:

        return Response({})
