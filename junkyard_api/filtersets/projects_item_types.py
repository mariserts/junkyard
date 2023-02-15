# -*- coding: utf-8 -*-
from typing import Type

from django.db.models.query import QuerySet

from django_filters import ChoiceFilter, FilterSet, NumberFilter

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

    for_user = NumberFilter(method='filter_by_for_user')
    used_by = ChoiceFilter(choices=CHOICES_USED_BY, method='filter_by_used_by')

    def filter_by_for_user(
        self: Type,
        queryset: QuerySet,
        name: str,
        value: str
    ) -> QuerySet:

        project_pk = self.request.parser_context['view'].kwargs.get(
            'project_pk',
            None
        )

        pset = self.request.user.permission_set

        if int(project_pk) not in pset.get_projects():
            return queryset.none()

        if pset.is_project_user(project_pk) is True:
            return queryset

        queryset = queryset.filter(
            for_tenants__pk=project_pk
        ).prefetch_related(
            'for_tenants'
        )

        return queryset

    def filter_by_used_by(
        self: Type,
        queryset: QuerySet,
        name: str,
        value: str
    ) -> QuerySet:

        project_pk = self.request.parser_context['view'].kwargs.get(
            'project_pk',
            None
        )

        if value == self.CHOICE_USED_BY_PROJECT[0]:
            queryset = queryset.filter(
                for_projects__pk=project_pk
            ).prefetch_related(
                'for_projects'
            )

        if value == self.CHOICE_USED_BY_TENANT[0]:
            queryset = queryset.filter(
                for_tenants__pk=project_pk
            ).prefetch_related(
                'for_tenants'
            )

        return queryset
