# -*- coding: utf-8 -*-
from typing import Final

from django.db.models import Q
from django.db.models.query import QuerySet

from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ..filtersets.tenant_admins import TenantAdminsFilterSet
from ..mixins import ViewSetKwargsMixin
from ..models import TenantAdmin
from ..permissions import TenantUserPermission
from ..serializers.tenant_admins import TenantAdminSerializer

from .base import BaseViewSet


class TenantAdminsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    ViewSetKwargsMixin,
    BaseViewSet
):

    filterset_class: Final = TenantAdminsFilterSet
    ordering_fields = ('-id', )
    permission_classes: Final = BaseViewSet.permission_classes + [
        TenantUserPermission, ]
    queryset: Final = TenantAdmin.objects.all()
    serializer_class: Final = TenantAdminSerializer

    def get_queryset(
        self: BaseViewSet,
    ) -> QuerySet:

        tenant_pk = self.kwargs.get('tenant_pk', None)
        user_id = self.request.user.id

        queryset = self.queryset.filter(
            tenant_id=tenant_pk
        )

        condition = Q()
        condition.add(Q(tenant__owner_id=user_id), Q.OR)
        condition.add(Q(tenant__admins__user_id=user_id), Q.OR)

        queryset = queryset.filter(
            condition
        ).select_related(
            'tenant',
        ).prefetch_related(
            'tenant__admins'
        )

        queryset = queryset.order_by(
            *self.ordering_fields
        ).distinct()

        return queryset

    def update(self, request, *args, **kwargs):

        try:
            request_data_tenant_pk = request.data['tenant']
        except KeyError:
            return Response('"tenant" is not provided')

        tenant_pk = self.get_kwarg_tenant_pk()

        if str(request_data_tenant_pk) != str(tenant_pk):
            raise ValidationError({
                'tenant': ['Tenant switching is not allowed']
            })

        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):

        try:
            request_data_tenant_pk = request.data['tenant']
        except KeyError:
            return Response('"tenant" is not provided')

        tenant_pk = self.get_kwarg_tenant_pk()

        if str(request_data_tenant_pk) != str(tenant_pk):
            raise ValidationError({
                'tenant': ['Tenant switching is not allowed']
            })

        return super().create(request, *args, **kwargs)
