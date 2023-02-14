# -*- coding: utf-8 -*-
from typing import Type

from django.db.models.query import QuerySet

from django_filters import ChoiceFilter, FilterSet

from ..models import ItemType


class ProjectsItemTypesFilterSet(FilterSet):

    CHOICE_USED_BY_PROJECT = ('project', 'Project')
    CHOICE_USED_BY_TENANT = ('tenant', 'Tenant')
    CHOICES_USED_BY = (
        CHOICE_USED_BY_PROJECT,
        CHOICE_USED_BY_TENANT
    )

    class Meta:
        model = ItemType
        fields = [
            'code',
            'is_active',
        ]

    used_by = ChoiceFilter(
        choices=CHOICES_USED_BY, method='filter_by_used_by')

    def filter_by_used_by(
        self: Type,
        queryset: QuerySet,
        name: str,
        value: str
    ) -> QuerySet:

        project_pk = self.request.kwargs.get('project_pk', None)

        if value == self.CHOICE_USED_BY_PROJECT[0]:
            queryset = queryset.exclude(
                for_tenants__pk=project_pk
            ).select_related(
                'for_tenants'
            )

        elif value == self.CHOICE_USED_BY_TENANT[0]:
            queryset = queryset.exclude(
                for_projects__pk=project_pk
            ).select_related(
                'for_projects'
            )

        return queryset
