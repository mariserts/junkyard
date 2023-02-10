# -*- coding: utf-8 -*-
from typing import Type

from django.db.models.query import QuerySet

from django_filters import CharFilter, FilterSet

from ..models import User


class ProjectsTenantsUsersFilterSet(FilterSet):

    class Meta:
        model = User
        fields = [
            'email'
        ]

    email = CharFilter(method='filter_by_email')

    def filter_by_email(
        self: Type,
        queryset: QuerySet,
        name: str,
        value: str,
    ) -> QuerySet:

        return queryset.filter(
            email=value.lower()
        )
