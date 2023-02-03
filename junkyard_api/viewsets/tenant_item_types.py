# -*- coding: utf-8 -*-
from typing import Final, Union

from django.db.models.query import QuerySet

from rest_framework.request import Request
from rest_framework.response import Response

from ..exceptions import ItemTypeNotFoundException, NoItemTypeAccessException
from ..mixins import ViewSetKwargsMixin
from ..models import Tenant
from ..permissions import TenantUserPermission
from ..serializers.item_types import ItemTypeSerializer

from .base import BaseViewSet


class TenantItemTypesViewSet(
    ViewSetKwargsMixin,
    BaseViewSet
):

    CACHE_TIMEOUT_IS_ROOT_TENANT = 5
    CACHE_TIMEOUT_LIST = 5

    permission_classes: Final = BaseViewSet.permission_classes + [
        TenantUserPermission, ]
    serializer_class: Final = ItemTypeSerializer
    queryset = QuerySet()

    def list(
        self: BaseViewSet,
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
            'results': self.serializer_class(item_types, many=True).data
        }

        return Response(data)

    def retrieve(
        self: BaseViewSet,
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

        return Response(self.serializer_class(item_type).data)
