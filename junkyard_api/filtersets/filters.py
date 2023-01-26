# -*- coding: utf-8 -*-
from django_filters import MultipleChoiceFilter
from .fields import EmptyCharField


class EmptyMultipleChoiceFilter(MultipleChoiceFilter):
    field_class = EmptyCharField
