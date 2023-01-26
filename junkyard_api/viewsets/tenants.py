# -*- coding: utf-8 -*-
from typing import Final

from django.db.models.query import QuerySet

from rest_framework import mixins, viewsets

from ..models import Tenant
from ..pagination import JunkyardApiPagination
from ..serializers.tenants import TenantSerializer


class TenantsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    model: Final = Tenant
    ordering_fields = ['id']
    pagination_class: Final = JunkyardApiPagination
    queryset: Final = model.objects.all()
    serializer_class: Final = TenantSerializer

    def get_queryset(
        self: viewsets.GenericViewSet,
    ) -> QuerySet:

        queryset = self.queryset.filter(
            owner_id=self.request.user.id
        ).order_by(
            *self.ordering_fields
        )

        return queryset
