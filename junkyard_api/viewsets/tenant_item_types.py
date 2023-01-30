# -*- coding: utf-8 -*-
from typing import Final, Union

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from ..exceptions import ItemTypeNotFoundException, NoItemTypeAccessException
from ..mixins import ViewSetKwargsMixin
from ..models import Tenant
from ..permissions import AuthenticatedUserPermission, TenantUserPermission
from ..serializers.item_types import ItemTypeSerializer


class TenantItemTypesViewSet(
    ViewSetKwargsMixin,
    viewsets.GenericViewSet
):

    CACHE_TIMEOUT_IS_ROOT_TENANT = 5
    CACHE_TIMEOUT_LIST = 5

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

        item_types = Tenant.get_tenant_item_types(tenant_pk)

        data = {
            'next': None,
            'previous': None,
            'page': 1,
            'pages': 1,
            'total': len(item_types),
            'results': ItemTypeSerializer(item_types, many=True).data
        }

        return Response(data)

    def retrieve(
        self: viewsets.GenericViewSet,
        request: Request,
        tenant_pk: int,
        pk: Union[None, int]
    ) -> Response:

        try:
            item_type = Tenant.get_tenant_item_type(tenant_pk, pk)
        except NoItemTypeAccessException:
            return Response('Access denied', status=403)
        except ItemTypeNotFoundException:
            return Response('Not found', status=404)

        return Response(ItemTypeSerializer(item_type).data)
