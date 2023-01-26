# -*- coding: utf-8 -*-
from django.forms import MultipleChoiceField


class EmptyCharField(MultipleChoiceField):
    def validate(self: MultipleChoiceField, value: str) -> bool:
        return True
