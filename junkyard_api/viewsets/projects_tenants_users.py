# -*- coding: utf-8 -*-
from typing import Type

from django.db.models.query import QuerySet

from rest_framework import mixins, permissions, viewsets

from django_filters import rest_framework as filters

from ..filtersets.projects_tenants_users import ProjectsTenantsUsersFilterSet
from ..models import User
from ..pagination import JunkyardApiPagination
from ..serializers.users import UserSerializer


class ProjectsTenantsUsersViewSetPermission(permissions.BasePermission):

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


class ProjectsTenantsUsersViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProjectsTenantsUsersFilterSet
    ordering_fields = ['email', ]
    pagination_class = JunkyardApiPagination
    permission_classes = (
        permissions.IsAuthenticated,
        ProjectsTenantsUsersViewSetPermission
    )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    swagger_schema = None

    # @action
    # invite user to become tenant user for this project
    # sends email with hashed data in a link

    def get_queryset(
        self: Type
    ) -> QuerySet:

        if self.request.user.is_authenticated is False:
            return User.objects.none()

        project_pk = self.kwargs['project_pk']

        queryset = self.queryset.filter(
            tenants__tenant__users__project__pk=project_pk,
            is_active=True,
        ).prefetch_related(
            'tenants__tenant__users__project'
        ).order_by(
            *self.ordering_fields
        )

        return queryset
