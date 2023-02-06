# -*- coding: utf-8 -*-
from django.db.models.query import QuerySet

from django_filters import BooleanFilter, FilterSet, NumberFilter

from ..models import User, Tenant


class TenantsFilterSet(FilterSet):

    all_predecessors_of = NumberFilter(method='filter_by_all_predecessors_of')
    all_successors_of = NumberFilter(method='filter_by_all_successors_of')
    is_root = BooleanFilter(method='filter_by_is_root')
    predecessors_of = NumberFilter(method='filter_by_predecessors_of')
    successors_of = NumberFilter(method='filter_by_successors_of')
    user = NumberFilter(method='filter_by_available_to_user_id')

    class Meta:
        model = Tenant
        fields = [
            'is_root',
        ]

    def filter_by_available_to_user_id(
        self,
        queryset: QuerySet,
        name: str,
        value: int
    ) -> QuerySet:
        tenant_ids = User.get_tenants(value, format='ids')
        queryset = queryset.filter(pk__in=tenant_ids)
        return queryset

    def filter_by_all_predecessors_of(
        self,
        queryset: QuerySet,
        name: str,
        value: int
    ) -> QuerySet:

        parents_ids = Tenant.get_all_parents_ids(int(value))

        queryset = queryset.filter(pk__in=parents_ids)

        return queryset

    def filter_by_all_successors_of(
        self,
        queryset: QuerySet,
        name: str,
        value: int
    ) -> QuerySet:

        children_ids = Tenant.get_all_children_ids(int(value))

        queryset = queryset.filter(pk__in=children_ids)

        return queryset

    def filter_by_is_root(
        self,
        queryset: QuerySet,
        name: str,
        value: int
    ) -> QuerySet:

        queryset = queryset.filter(parent__isnull=value)

        return queryset

    def filter_by_predecessors_of(
        self,
        queryset: QuerySet,
        name: str,
        value: int
    ) -> QuerySet:

        queryset = queryset.filter(parent_id=int(value))

        return queryset

    def filter_by_successors_of(
        self,
        queryset: QuerySet,
        name: str,
        value: int
    ) -> QuerySet:

        queryset = queryset.filter(
            children__id=int(value)
        ).prefetch_related(
            'children'
        )

        return queryset
