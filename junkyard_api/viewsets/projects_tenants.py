# -*- coding: utf-8 -*-
from typing import Type

from django.db.models.query import QuerySet

from rest_framework import mixins, permissions, viewsets

from django_filters import rest_framework as filters

from ..filtersets.projects_tenants import ProjectsTenantsFilterSet
from ..models import Tenant
from ..pagination import JunkyardApiPagination
from ..serializers.tenants import TenantSerializer


class ProjectsTenantsViewSetPermission(
    permissions.BasePermission
):

    def has_permission(
        self: Type,
        request: Type,
        view: Type
    ):

        if request.method not in permissions.SAFE_METHODS:
            project_pk = view.kwargs['project_pk']
            return request.user.permission_set.is_project_user(project_pk)

        return True


class ProjectsTenantsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProjectsTenantsFilterSet
    ordering_fields = ('id', )
    pagination_class = JunkyardApiPagination
    permission_classes = (
        permissions.IsAuthenticated,
        ProjectsTenantsViewSetPermission,
    )
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    def get_queryset(
        self: Type,
    ) -> QuerySet:

        if self.request.user.is_authenticated is False:
            return Tenant.objects.none()

        project_pk = self.kwargs['project_pk']

        queryset = self.queryset.filter(
            projects__project__pk=project_pk,
        ).prefetch_related(
            'projects__project',
        ).order_by(
            *self.ordering_fields
        )

        return queryset
