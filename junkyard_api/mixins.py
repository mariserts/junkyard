# -*- coding: utf-8 -*-
from rest_framework import viewsets


class ViewSetPayloadMixin:

    def get_payload_tenant(
        self: viewsets.GenericViewSet,
        default: None = None,
    ) -> int:
        return self.request.data.get('tenant', default)


class ViewSetKwargsMixin:

    def get_kwarg_item_pk(
        self: viewsets.GenericViewSet,
        default: None = None,
    ) -> str:
        return self.kwargs.get('item_pk', default)

    def get_kwarg_tenant_pk(
        self: viewsets.GenericViewSet,
        default: None = None,
    ) -> str:
        return self.kwargs.get('tenant_pk', default)
