# -*- coding: utf-8 -*-
from django_filters import FilterSet

from ..models import ItemType


class ItemTypesFilterSet(FilterSet):

    class Meta:
        model = ItemType
        fields = [
            'code',
            'is_active',
        ]
