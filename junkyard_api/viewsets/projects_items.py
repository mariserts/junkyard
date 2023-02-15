# -*- coding: utf-8 -*-
from datetime import datetime, timezone
from typing import List, Type, Union

from django.db.models import Q
from django.db.models.query import QuerySet

from rest_framework import mixins, permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from django_filters import rest_framework as filters

from ..clients.http import HttpRequest
from ..filtersets.projects_items import ProjectsItemsFilterSet
from ..models import Item
from ..pagination import JunkyardApiPagination
from ..serializers.items import ItemSerializer
from ..utils.urls import get_projects_tenants_items_url


class ProjectsItemsViewSetPermission(permissions.BasePermission):

    def has_permission(
        self: Type,
        request: Type,
        view: Type
    ):

        if request.method not in permissions.SAFE_METHODS:

            tenant_id = request.data.get('tenant', None)
            project_pk = view.kwargs['project_pk']

            pset = request.user.permission_set

            if tenant_id is None:
                return pset.is_project_user(project_pk)

            return pset.is_project_tenant_user(project_pk, tenant_id)

        return True


class ProjectsItemsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProjectsItemsFilterSet
    ordering_fields = ('-id', )
    pagination_class = JunkyardApiPagination
    permission_classes = (
        permissions.IsAuthenticated,
        ProjectsItemsViewSetPermission,
    )
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

        condition = Q()
        condition.add(
            Q(
                tenant_id__in=pset.get_project_tenants(project_pk)
            ),
            Q.OR
        )
        condition.add(
            Q(
                published_at__lt=datetime.now(timezone.utc),
                published=True,
            ),
            Q.OR
        )

        queryset = queryset.filter(
            condition
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
            url = self._get_projects_tenants_items_url(tenant_id, detail=False)
            return self._proxy('POST', url)

        return super().create(request, *args, **kwargs)

    def destroy(
        self: Type,
        request: Type,
        *args: List,
        **kwargs: dict
    ) -> Type[Response]:

        item_pk = kwargs['id']

        object = Item.objects.get(pk=item_pk)

        tenant_id = object.tenant_id

        if tenant_id is not None:
            url = self._get_projects_tenants_items_url(
                tenant_id,
                item_pk=item_pk
            )
            return self._proxy('DELETE', url)

        return super().destroy(request, *args, **kwargs)

    def partial_update(
        self: Type,
        request: Type,
        *args: List,
        **kwargs: dict
    ) -> Type[Response]:

        self._validate_request()

        item_pk = kwargs['id']
        tenant_id = request.data.get('tenant', None)

        if tenant_id is not None:
            url = self._get_projects_tenants_items_url(
                tenant_id,
                item_pk=item_pk
            )
            return self._proxy('PATCH', url)

        return super().partial_update(request, *args, **kwargs)

    def update(
        self: Type,
        request: Type,
        *args: List,
        **kwargs: dict
    ) -> Type[Response]:

        self._validate_request()

        item_pk = kwargs['id']
        tenant_id = request.data.get('tenant', None)

        if tenant_id is not None:
            url = self._get_projects_tenants_items_url(
                tenant_id,
                item_pk=item_pk
            )
            return self._proxy('PUT', url)

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

    def _proxy(
        self: Type,
        method: str,
        url: str
    ) -> Type[Response]:

        request = HttpRequest().request(
            data=self.request.data,
            format='request',
            headers=self.request.META,
            method=method,
            url=f'{self._get_full_request_hostname}{url}'
        )

        if request.ok() is True:

            return Response(
                request.json(),
                status=request.status_code
            )

        return Response(
            request.text,
            status=request.status_code
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

    def _get_full_request_hostname(
        self: Type,
    ) -> str:
        hostname = 'http'
        if self.request.is_secure is True:
            hostname += 's'
        hostname += '://'
        hostname += self.request.get_host()
        return hostname
