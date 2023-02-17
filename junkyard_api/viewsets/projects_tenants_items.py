# -*- coding: utf-8 -*-
from typing import List, Type

from django.db.models.query import QuerySet

from rest_framework import mixins, permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

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

            tenant_pk = view.kwargs['tenant_pk']
            project_pk = view.kwargs['project_pk']

            pset = request.user.permission_set

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
    swagger_schema = None

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
            is_active=True,
        )

        return queryset

    def create(
        self: Type,
        request: Type,
        *args: List,
        **kwargs: dict
    ) -> Type[Response]:

        self._validate_request()

        return super().create(request, *args, **kwargs)

    def partial_update(
        self: Type,
        request: Type,
        *args: List,
        **kwargs: dict
    ) -> Type[Response]:

        self._validate_request()

        return super().partial_update(request, *args, **kwargs)

    def update(
        self: Type,
        request: Type,
        *args: List,
        **kwargs: dict
    ) -> Type[Response]:

        self._validate_request()

        return super().update(request, *args, **kwargs)

    def _validate_request(
        self: Type
    ) -> None:

        project_id = self.request.data.get('project', None)
        project_pk = self.kwargs.get('project_pk', None)

        if str(project_id) != str(project_pk):
            raise ValidationError(
                'Can not update items from other projects',
                code=400
            )

        tenant_id = self.request.data.get('tenant', None)
        tenant_pk = self.kwargs.get('tenant_pk', None)

        if str(tenant_id) != str(tenant_pk):
            raise ValidationError(
                'Can not update items from other tenants',
                code=400
            )

        item_type = self.request.data.get('item_type', None)
        pset = self.request.user.permission_set

        has_access = pset.has_access_to_project_item_type(
            project_id,
            item_type
        )

        if has_access is False:
            raise ValidationError(
                f'No access to item type "{item_type}" in this project',
                code=403
            )
