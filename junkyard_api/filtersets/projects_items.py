# -*- coding: utf-8 -*-
from typing import Type

from django.db.models.query import QuerySet

from django_filters import ChoiceFilter, FilterSet

from ..models import Item


class ProjectsItemsFilterSet(FilterSet):

    class Meta:
        model = Item
        fields = [
            'item_type',
        ]

    CHOICES_ACTION_UPDATE = ('update', 'Update')
    CHOICES_ACTION = (
        CHOICES_ACTION_UPDATE,
    )

    action = ChoiceFilter(method='filter_by_action', choices=CHOICES_ACTION)

    def get_project_pk(
        self: Type
    ) -> int:
        return self.request.parser_context['kwargs']['project_pk']

    def filter_by_action(
        self: Type,
        queryset: QuerySet,
        name: str,
        value: str,
    ) -> QuerySet:

        user = self.request.user

        if user.is_authenticated is False:
            return queryset

        project_pk = self.get_project_pk()
        pset = user.permission_set

        user_is_project_user = pset.is_project_user(project_pk)
        if user_is_project_user is True:
            return True

        if value == self.CHOICES_ACTION_UPDATE[0]:
            tenant_ids = pset.get_project_tenants(project_pk)
            return queryset.filter(tenant_id__in=tenant_ids)

        return queryset
