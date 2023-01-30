# -*- coding: utf-8 -*-
from typing import Union

from django.db.models.query import QuerySet

from django_filters import FilterSet

from ..models import TenantAdmin

from .filters import EmptyMultipleChoiceFilter


class TenantAdminsFilterSet(FilterSet):

    email = EmptyMultipleChoiceFilter(method='filter_by_email')

    class Meta:
        model = TenantAdmin
        fields = [
            'email',
        ]

    def filter_by_email(
        self,
        queryset: QuerySet,
        name: str,
        value: Union[str, None]
    ) -> QuerySet:

        queryset = queryset.filter(
            user__email__in=value
        ).prefetch_related(
            'user',
        )

        return queryset
