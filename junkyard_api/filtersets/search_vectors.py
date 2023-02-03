# -*- coding: utf-8 -*-
from typing import List

from django.db.models import Q


class BaseConditionGenerator:
    pass


class SearchVectorConditionGenerator(BaseConditionGenerator):

    #
    # /?filter=translatable_content__title:Hello World
    # /?filter=translatable_content__title__iexact:Hello World
    # /?filter=translatable_content__title__in:one,two,three
    #

    filter_strings = []

    def __init__(
        self: BaseConditionGenerator,
        filter_strings: List[str],
    ) -> None:
        self.filter_strings = filter_strings

    def get_exact_condition(
        self: BaseConditionGenerator,
        filter_parts: List[str],
        case_sensetive: bool = False
    ) -> Q:

        lookup = 'exact'

        field = filter_parts[0]
        value = filter_parts[1]

        if case_sensetive is True:
            lookup = f'i{lookup}'

        field = str(field).replace(f'__{lookup}', '')

        return Q(**{
            'search_vectors__field_name': field,
            f'search_vectors__raw_value__{lookup}': value
        })

    def get_in_condition(
        self: BaseConditionGenerator,
        filter_parts: List[str],
        sepatrator: str = ','
    ) -> Q:

        field = str(filter_parts[0]).replace('__in')
        value = str(filter_parts[1]).split(',')

        return Q(**{
            'search_vectors__field_name': field,
            'search_vectors__raw_value__in': value.split(sepatrator)
        })

    def get_contains_condition(
        self: BaseConditionGenerator,
        filter_parts: List[str],
        case_sensetive: bool = False
    ) -> Q:

        lookup = 'contains'

        field = filter_parts[0]
        value = filter_parts[1]

        if case_sensetive is True:
            lookup = f'i{lookup}'

        field = str(field).replace(f'__{lookup}', '')

        return Q(**{
            'search_vectors__field_name': field,
            f'search_vectors__raw_value__{lookup}': value
        })

    def get_in_endswith(
        self: BaseConditionGenerator,
        filter_parts: List[str],
        case_sensetive: bool = False
    ) -> Q:

        lookup = 'endswith'

        field = filter_parts[0]
        value = filter_parts[1]

        if case_sensetive is True:
            lookup = f'i{lookup}'

        field = str(field).replace(f'__{lookup}', '')

        return Q(**{
            'search_vectors__field_name': field,
            f'search_vectors__raw_value__{lookup}': value
        })

    def get_in_startswith(
        self: BaseConditionGenerator,
        filter_parts: List[str],
        case_sensetive: bool = False
    ) -> Q:

        lookup = 'startswith'

        field = filter_parts[0]
        value = filter_parts[1]

        if case_sensetive is True:
            lookup = f'i{lookup}'

        field = str(field).replace(f'__{lookup}', '')

        return Q(**{
            'search_vectors__field_name': field,
            f'search_vectors__raw_value__{lookup}': value
        })

    def get_condition(
        self: BaseConditionGenerator,
        string: str,
    ) -> Q:

        filter_parts = string.split(':')

        field = filter_parts[0]
        value = filter_parts[1]

        if field.endswith('__exact') is True:
            return self.get_exact_condition(filter_parts)

        if field.endswith('__iexact') is True:
            return self.get_exact_condition(filter_parts, True)

        if field.endswith('__in') is True:
            return self.get_in_condition(filter_parts)

        if field.endswith('__contains') is True:
            return self.get_contains_condition(filter_parts)

        if field.endswith('__icontains') is True:
            return self.get_contains_condition(filter_parts, True)

        if field.endswith('__startswith') is True:
            return self.get_startswith_condition(filter_parts)

        if field.endswith('__istartswith') is True:
            return self.get_startswith_condition(filter_parts, True)

        if field.endswith('__endswith') is True:
            return self.get_endswith_condition(filter_parts)

        if field.endswith('__endswith') is True:
            return self.get_endswith_condition(filter_parts, True)

        return Q(
            search_vectors__field_name=field,
            search_vectors__raw_value=value
        )

    def get_conditions(
        self: BaseConditionGenerator
    ) -> Q:

        conditions = Q()

        for string in self.filter_strings:
            conditions.add(self.get_condition(string), Q.AND)

        return conditions
