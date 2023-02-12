# -*- coding: utf-8 -*-
from datetime import datetime, timezone
from typing import Type

from django.db.models import Q
from django.db.models.query import QuerySet

from rest_framework import mixins, permissions, viewsets
from django_filters import rest_framework as filters

from ..filtersets.projects_items import ProjectsItemsFilterSet
from ..models import Item
from ..pagination import JunkyardApiPagination
from ..serializers.items import ItemSerializer


class ProjectsItemsViewSetPermission(permissions.BasePermission):

    def has_permission(
        self: Type,
        request: Type,
        view: Type
    ):

        if request.method not in permissions.SAFE_METHODS:
            project_pk = view.kwargs['project_pk']
            return request.user.permission_set.is_project_user(project_pk)

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
