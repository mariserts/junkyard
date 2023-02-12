# -*- coding: utf-8 -*-
# from typing import Type, Union

# from django.db.models.query import QuerySet

from django_filters import FilterSet

from ..models import Tenant

# from .filters import EmptyMultipleChoiceFilter


class ProjectsTenantsFilterSet(FilterSet):

    class Meta:
        model = Tenant
        fields = []
