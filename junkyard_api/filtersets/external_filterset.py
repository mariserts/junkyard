# -*- coding: utf-8 -*-
from typing import Any, Type

from django.db.models import Q as DjQ


class ExternalFilterSet:

    item_type = None

    Q = DjQ

    CONNECTOR_AND = Q.AND
    CONNECTOR_OR = Q.OR
    CONNECTOR_XOR = Q.XOR

    def get_filter_for(
        self: Type,
        method: str,
    ) -> Any:

        _method = getattr(self, method, None)
        if _method is None:
            return None

        return _method

    def is_active(
        self: Type,
        condition: Type[DjQ],
        value: bool,
        connector: str = 'AND'
    ) -> Type[DjQ]:

        if connector == 'OR':
            _connector = self.CONNECTOR_AND
        elif connector == 'XOR':
            _connector = self.CONNECTOR_OR
        else:
            _connector = self.CONNECTOR_XOR

        condition.add(
            self.Q(
                item_type__code=self.item_type,
                is_active=True,
            ),
            _connector
        )

        return condition
