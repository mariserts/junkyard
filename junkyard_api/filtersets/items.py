# -*- coding: utf-8 -*-
from typing import Union

from django.db.models.query import QuerySet

from django_filters import FilterSet

from ..conf import settings
from ..models import Item

from .filters import EmptyMultipleChoiceFilter


class ItemsFilterSet(FilterSet):

    class Meta:
        model = Item
        fields = [
            'item_type',
        ]

    item_type = EmptyMultipleChoiceFilter(method='filter_by_item_type')

    def filter_by_item_type(
        self,
        queryset: QuerySet,
        name: str,
        value: Union[str, None]
    ) -> QuerySet:

        # url/?item_type=1&item_type=2
        # https://www.rfc-editor.org/rfc/rfc3986

        allowed_types = settings.ITEM_TYPE_REGISTRY.get_types(format='names')

        if len(value) == 0:
            return queryset

        item_types = list(set(allowed_types).intersection(set(value)))

        count = len(item_types)

        if count == 0:
            queryset = queryset.filter(item_type='--1')

        elif count == 1:
            queryset = queryset.filter(item_type=item_types[0])

        else:
            queryset = queryset.filter(item_type__in=item_types)

        return queryset.distinct()
