# -*- coding: utf-8 -*-
from typing import Type, Union

from django.db.models.query import QuerySet

from django_filters import FilterSet, NumberFilter


class ItemTypesFilterSet(FilterSet):

    tenant = NumberFilter(method='filter_by_tenant')

    def filter_by_tenant(
        self: Type,
        queryset: QuerySet,
        name: str,
        value: Union[int, None]
    ) -> QuerySet:

        return queryset
