# -*- coding: utf-8 -*-
from typing import Union

from django.db.models.query import QuerySet

from django_filters import FilterSet, NumberFilter

from ..models import User

from .filters import EmptyMultipleChoiceFilter


class UsersFilterSet(FilterSet):

    email = EmptyMultipleChoiceFilter(method='filter_by_email')
    owner_of = NumberFilter(method='filter_by_owner_of')
    admin_of = NumberFilter(method='filter_by_admin_of')

    class Meta:
        model = User
        fields = [
            'email',
        ]

    def filter_by_admin_of(
        self,
        queryset: QuerySet,
        name: str,
        value: int
    ) -> QuerySet:

        queryset = queryset.filter(
            tenants_to_admin__pk=value
        ).prefetch_related(
            'tenants_to_admin'
        )

        return queryset

    def filter_by_email(
        self,
        queryset: QuerySet,
        name: str,
        value: Union[str, None]
    ) -> QuerySet:

        queryset = queryset.filter(
            email__in=value
        )

        return queryset

    def filter_by_owner_of(
        self,
        queryset: QuerySet,
        name: str,
        value: int
    ) -> QuerySet:

        queryset = queryset.filter(
            tenants__pk=value
        ).prefetch_related(
            'tenants'
        )

        return queryset
