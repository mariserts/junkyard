# -*- coding: utf-8 -*-
from typing import Type, Union

from django.db.models.query import QuerySet

from django_filters import FilterSet

from ..models import ItemRelation

from .filters import EmptyMultipleChoiceFilter


class ItemRelationsFilterSet(FilterSet):

    class Meta:
        model = ItemRelation
        fields = [
            'label',
        ]

    label = EmptyMultipleChoiceFilter(method='filter_by_label')

    def filter_by_label(
        self: Type,
        queryset: QuerySet,
        name: str,
        value: Union[int, None]
    ) -> QuerySet:

        if len(value) == 0:
            queryset = queryset.filter(label='--1')
        else:
            queryset = queryset.filter(label__in=value)

        return queryset.distinct()
