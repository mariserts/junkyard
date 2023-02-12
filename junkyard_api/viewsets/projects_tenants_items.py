# -*- coding: utf-8 -*-
from datetime import datetime, timezone
from typing import Type

from django.db.models.query import QuerySet

from rest_framework import mixins, permissions, viewsets

from django_filters import rest_framework as filters

from ..filtersets.items import ItemsFilterSet
from ..models import Item
from ..pagination import JunkyardApiPagination
from ..serializers.items import ItemSerializer


class ProjectsTenantsItemsViewSetPermission(permissions.BasePermission):

    def has_permission(
        self: Type,
        request: Type,
        view: Type
    ):

        if request.method not in permissions.SAFE_METHODS:

            project_pk = view.kwargs['project_pk']
            tenant_pk = view.kwargs['tenant_pk']

            pset = request.user.permission_set

            if pset.is_project_user(project_pk) is True:
                return True

            return pset.is_project_tenant_user(project_pk, tenant_pk)

        return True


class ProjectsTenantsItemsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ItemsFilterSet
    ordering_fields = ('id', )
    pagination_class = JunkyardApiPagination
    permission_classes = (
        permissions.IsAuthenticated,
        ProjectsTenantsItemsViewSetPermission,
    )
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(
        self: Type
    ) -> QuerySet:

        if self.request.user.is_authenticated is False:
            return Item.objects.none()

        project_pk = self.kwargs['project_pk']
        tenant_pk = self.kwargs['tenant_pk']
        pset = self.request.user.permission_set

        queryset = self.queryset.filter(
            project__pk=project_pk,
            tenant__pk=tenant_pk,
        ).select_related(
            'project',
            'tenant',
        ).order_by(
            *self.ordering_fields
        )

        if pset.is_project_user(project_pk) is True:
            return queryset

        if pset.is_project_tenant_user(project_pk, tenant_pk) is True:
            return queryset

        queryset = queryset.filter(
            published=True,
            published_at__lt=datetime.now(timezone.utc),
        )

        return queryset
