# -*- coding: utf-8 -*-
from typing import List, Type

from django import forms


class ItemsFilterForm(
    forms.Form
):

    keyword = forms.CharField(required=False)
    item_type = forms.ChoiceField(choices=[])
    status = forms.ChoiceField(choices=[])
    tenant = forms.ChoiceField(choices=[])

    def __init__(
        self: Type,
        *args: List,
        **kwargs: dict
    ):

        item_type_choices = kwargs.pop('item_type_choices')
        status_choices = kwargs.pop('status_choices')
        tenant_choices = kwargs.pop('tenant_choices')

        super(ItemsFilterForm, self).__init__(*args, **kwargs)

        self.fields['item_type'] = forms.ChoiceField(
            choices=item_type_choices,
            required=False,
            initial=''
        )

        self.fields['status'] = forms.ChoiceField(
            choices=status_choices,
            required=False,
            initial=''

        )
        self.fields['tenant'] = forms.ChoiceField(
            choices=tenant_choices,
            required=False,
            initial=''
        )
