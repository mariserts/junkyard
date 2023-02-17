# -*- coding: utf-8 -*-
from typing import List, Type, Union

from django.db.models.query import QuerySet

from rest_framework import mixins, permissions, viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

from django_filters import rest_framework as filters

from ..filtersets.projects_items import ProjectsItemsFilterSet
from ..models import Item
from ..pagination import JunkyardApiPagination
from ..serializers.items import ItemSerializer
from ..utils.urls import get_projects_tenants_items_url

from .mixins import ProxyMixin


class ProjectsItemsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    ProxyMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProjectsItemsFilterSet
    ordering_fields = ('-id', )
    pagination_class = JunkyardApiPagination
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(
        self: Type
    ) -> QuerySet:

        if self.request.user.is_authenticated is False:
            return Item.objects.none()

        project_pk = self.kwargs['project_pk']
        pset = self.request.user.permission_set

        queryset = self.queryset.filter(
            project__pk=project_pk,
        ).select_related(
            'project',
        ).order_by(
            *self.ordering_fields
        )

        if pset.is_project_user(project_pk) is True:
            return queryset

        queryset = queryset.filter(
            tenant_id__in=pset.get_project_tenants(project_pk)
        )

        return queryset

    def create(
        self: Type,
        request: Type,
        *args: List,
        **kwargs: dict
    ) -> Type[Response]:

        self._validate_request()

        tenant_id = request.data.get('tenant', None)
        if tenant_id is not None:
            url = self._get_full_request_hostname
            url += self._get_projects_tenants_items_url(
                tenant_id, detail=False)
            return self._proxy(url)

        return super().create(request, *args, **kwargs)

    def destroy(
        self: Type,
        request: Type,
        *args: List,
        **kwargs: dict
    ) -> Type[Response]:

        self._validate_request()

        tenant_id = self._object.tenant_id

        if tenant_id is not None:
            url = self._get_full_request_hostname
            url += self._get_projects_tenants_items_url(
                tenant_id,
                item_pk=kwargs['pk']
            )
            return self._proxy(url)

        return super().destroy(request, *args, **kwargs)

    def partial_update(
        self: Type,
        request: Type,
        *args: List,
        **kwargs: dict
    ) -> Type[Response]:

        self._validate_request()

        item_pk = kwargs['pk']
        tenant_id = request.data.get('tenant', None)

        if tenant_id is not None:
            url = self._get_full_request_hostname
            url += self._get_projects_tenants_items_url(
                tenant_id,
                item_pk=item_pk
            )
            return self._proxy(url)

        return super().partial_update(request, *args, **kwargs)

    def update(
        self: Type,
        request: Type,
        *args: List,
        **kwargs: dict
    ) -> Type[Response]:

        self._validate_request()

        item_pk = kwargs['pk']
        tenant_id = request.data.get('tenant', None)

        if tenant_id is not None:
            url = self._get_full_request_hostname
            url += self._get_projects_tenants_items_url(
                tenant_id,
                item_pk=item_pk
            )
            return self._proxy(url)

        return super().update(request, *args, **kwargs)

    def _validate_request(
        self: Type
    ) -> None:

        project_pk = self.kwargs.get('project_pk', None)
        item_pk = self.kwargs.get('pk', None)

        #
        #
        #

        if self.action == 'destroy':

            try:
                self._object = Item.objects.get(
                    project__pk=project_pk,
                    pk=item_pk
                )
            except Item.DoesNotExist:
                raise NotFound(f'Item "ID:{item_pk}" not found')

            tenant_id = self._object.tenant_id
            project_id = self._object.project_id

        else:
            tenant_id = self.request.data.get('tenant', None)
            project_id = self.request.data.get('project', None)

        if str(project_id) != str(project_pk):
            raise PermissionDenied('Can not update items from other projects')

        #
        #
        #

        pset = self.request.user.permission_set

        if tenant_id is None:
            if pset.is_project_user(project_pk) is False:
                raise PermissionDenied(
                    f'No access to project "ID:{project_pk}" items',
                )

        else:
            if pset.is_project_tenant_user(project_pk, tenant_id) is False:
                raise PermissionDenied(
                    f'No access to tenant "ID:{tenant_id}" items',
                )

        if self.action != 'destroy':

            item_type = self.request.data.get('item_type', None)

            has_access = pset.has_access_to_project_item_type(
                project_id,
                item_type
            )

            if has_access is False:
                raise PermissionDenied(
                    f'No access to item type "{item_type}" in this project',
                )

    def _get_projects_tenants_items_url(
        self: Type,
        tenant_pk: Union[int, str],
        item_pk: Union[None, int, str] = None
    ) -> str:

        return get_projects_tenants_items_url(
            self.request,
            self.kwargs['project_pk'],
            tenant_pk,
            item_pk=item_pk,
        )
