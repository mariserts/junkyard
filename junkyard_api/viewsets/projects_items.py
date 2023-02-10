# -*- coding: utf-8 -*-
from typing import Type

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

        if request.method in permissions.SAFE_METHODS:

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

        return self.request.user.get_project_items(project_pk)
