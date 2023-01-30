# -*- coding: utf-8 -*-
from typing import Final

from django.db.models import Q
from django.db.models.query import QuerySet

from rest_framework import mixins, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from django_filters import rest_framework as filters

from ..filtersets.tenant_admins import TenantAdminsFilterSet
from ..mixins import ViewSetKwargsMixin
from ..models import TenantAdmin
from ..pagination import JunkyardApiPagination
from ..permissions import AuthenticatedUserPermission, TenantUserPermission
from ..serializers.tenant_admins import TenantAdminSerializer


class TenantAdminsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    ViewSetKwargsMixin,
    viewsets.GenericViewSet
):

    filter_backends: Final = (filters.DjangoFilterBackend, )
    filterset_class = TenantAdminsFilterSet
    model: Final = TenantAdmin
    ordering_fields = ('-id', )
    pagination_class: Final = JunkyardApiPagination
    permission_classes: Final = [
        AuthenticatedUserPermission,
        TenantUserPermission,
    ]
    queryset: Final = model.objects.all()
    serializer_class: Final = TenantAdminSerializer

    def get_queryset(
        self: viewsets.GenericViewSet,
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
