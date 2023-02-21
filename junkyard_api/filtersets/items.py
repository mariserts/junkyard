# -*- coding: utf-8 -*-
from typing import Union

from django.db.models import Q
from django.db.models.query import QuerySet

from django_filters import BooleanFilter, FilterSet, IsoDateTimeFilter

from ..conf import settings
from ..models import Item

from .filters import EmptyMultipleChoiceFilter


class ItemsFilterSet(FilterSet):

    class Meta:
        model = Item
        fields = [
            'item_type',
        ]

    active_before = IsoDateTimeFilter(method='filter_by_active_before')
    is_active = BooleanFilter(method='filter_by_is_active')
    item_type = EmptyMultipleChoiceFilter(method='filter_by_item_type')

    def filter_by_active_before(
        self,
        queryset: QuerySet,
        name: str,
        value: bool
    ) -> QuerySet:

        condition = Q()
        condition.add(Q(data__active_from__lte=str(value)), Q.OR)
        condition.add(Q(data__active_from__isnull=True), Q.OR)

        queryset = queryset.filter(condition)

        return queryset.distinct()

    def filter_by_is_active(
        self,
        queryset: QuerySet,
        name: str,
        value: bool
    ) -> QuerySet:

        queryset = queryset.filter(
            data__is_active=True
        )

        return queryset

    def filter_by_item_type(
        self,
        queryset: QuerySet,
        name: str,
        value: Union[str, None]
    ) -> QuerySet:

        allowed_types = settings.ITEM_TYPE_REGISTRY.get_types(format='codes')

        item_types = list(set(allowed_types).intersection(set(value)))

        count = len(item_types)

        if count == 0:
            queryset = queryset.filter(item_type__code='--1')

        elif count == 1:
            queryset = queryset.filter(item_type__code=item_types[0])

        else:
            queryset = queryset.filter(item_type__code__in=item_types)

        queryset = queryset.select_related(
            'item_type'
        )

        return queryset.distinct()
