# -*- coding: utf-8 -*-
from typing import Type, Union

from django.db.models.query import QuerySet

from django_filters import ChoiceFilter, FilterSet

from ..models import Project

from .filters import EmptyMultipleChoiceFilter


class ProjectsFilterSet(FilterSet):

    CHOICES_ACTION_CREATE_ITEMS = ('create_items', 'Create items')
    CHOICES_ACTION_UPDATE = ('update', 'Update')
    CHOICES_ACTION = (
        CHOICES_ACTION_CREATE_ITEMS,
        CHOICES_ACTION_UPDATE,
    )

    class Meta:
        model = Project
        fields = []

    id = EmptyMultipleChoiceFilter(method='filter_by_id')
    action = ChoiceFilter(method='filter_by_action', choices=CHOICES_ACTION)

    def filter_by_id(
        self: Type[FilterSet],
        queryset: Type[QuerySet],
        name: str,
        value: Union[str, None]
    ) -> QuerySet:

        ids = []
        for id in value:
            if id.isdigit() is True:
                ids.append(int(id))

        project_ids = self.request.user.permission_set.get_projects()

        if -1 in project_ids:
            return queryset

        if len(ids) == 0:
            return queryset.filter(id__in=project_ids)

        ids = list(set(ids).intersection(set(project_ids)))

        if len(ids) > 0:
            return queryset.filter(id__in=project_ids)

        return queryset

    def filter_by_action(
        self: Type,
        queryset: QuerySet,
        name: str,
        value: str,
    ) -> QuerySet:

        if self.request.user.is_authenticated is False:
            return queryset.none()

        if value == self.CHOICES_ACTION_CREATE_ITEMS[0]:
            project_ids = self.request.user.permission_set.get_projects()
            queryset = queryset.filter(id__in=project_ids)

        return queryset
