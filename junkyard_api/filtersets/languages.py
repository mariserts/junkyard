# -*- coding: utf-8 -*-
from typing import Union

from django.db.models.query import QuerySet

from django_filters import BooleanFilter, FilterSet


class LanguagesFilterSet(FilterSet):

    default = BooleanFilter(method='filter_by_default')

    def filter_by_default(
        self,
        queryset: QuerySet,
        name: str,
        value: Union[bool, None]
    ) -> QuerySet:

        return queryset
