# -*- coding: utf-8 -*-
from typing import Type

from django.db.models import Q
from django.db.models.query import QuerySet

from rest_framework import mixins, permissions, viewsets

from django_filters import rest_framework as filters

from ..filtersets.projects_users import ProjectsUsersFilterSet
from ..models import User
from ..pagination import JunkyardApiPagination
from ..serializers.users import UserSerializer


class ProjectsUsersViewSetPermission(permissions.BasePermission):

    def has_permission(
        self: Type,
        request: Type,
        view: Type
    ):

        if request.method not in permissions.SAFE_METHODS:
            project_pk = view.kwargs['pk']
            return request.user.permission_set.is_project_user(project_pk)

        return True


class ProjectsUsersViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProjectsUsersFilterSet
    ordering_fields = ['id', 'email', ]
    pagination_class = JunkyardApiPagination
    permission_classes = (
        permissions.IsAuthenticated,
        ProjectsUsersViewSetPermission,
    )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # @action
    # invite user to become project user
    # sends email with hashed data in a link

    def get_queryset(
        self: Type,
    ) -> QuerySet:

        if self.request.user.is_authenticated is False:
            return User.objects.none()

        project_pk = self.kwargs['project_pk']

        condition = Q()
        condition.add(Q(projects__project__pk=project_pk), Q.OR)
        condition.add(Q(tenants__tenant__users__project__pk=project_pk), Q.OR)

        queryset = self.queryset.filter(
            condition
        ).prefetch_related(
            'projects__project',
            'tenants__tenant__users__project',
        )

        queryset = queryset.filter(
            is_active=True
        ).order_by(
            *self.ordering_fields
        )

        return queryset
