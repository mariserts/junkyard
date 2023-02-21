# -*- coding: utf-8 -*-
from typing import Type

from django.db.models.query import QuerySet

from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, viewsets

from ..filtersets.projects import ProjectsFilterSet
from ..models import Project
from ..pagination import JunkyardApiPagination
from ..serializers.projects import ProjectSerializer


class ProjectsViewSetPermission(permissions.BasePermission):

    def has_permission(
        self: Type,
        request: Type,
        view: Type
    ):

        if view.action == 'create':
            return request.user.is_superuser

        if request.method not in permissions.SAFE_METHODS:
            project_pk = view.kwargs['pk']
            return request.user.permission_set.is_project_user(project_pk)

        return True


class ProjectsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProjectsFilterSet
    ordering_fields = ['name', ]
    pagination_class = JunkyardApiPagination
    permission_classes = (
        permissions.IsAuthenticated,
        ProjectsViewSetPermission,
    )
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(
        self: Type,
    ) -> QuerySet:

        if self.request.user.is_authenticated is False:
            return Project.objects.none()

        return self.queryset.order_by(
            *self.ordering_fields
        )
