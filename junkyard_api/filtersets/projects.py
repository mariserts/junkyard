# -*- coding: utf-8 -*-
from typing import Type, Union

from django.db.models.query import QuerySet

from django_filters import FilterSet

from ..models import Project

from .filters import EmptyMultipleChoiceFilter


class ProjectsFilterSet(FilterSet):

    class Meta:
        model = Project
        fields = []

    id = EmptyMultipleChoiceFilter(method='filter_by_id')

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
