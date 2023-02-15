# -*- coding: utf-8 -*-
from django import forms


class ProjectsFilterForm(
    forms.Form
):

    keyword = forms.CharField(required=False)
