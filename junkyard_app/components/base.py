# -*- coding: utf-8 -*-
from typing import Type

from django.template.loader import render_to_string


class BaseComponent:

    request = None
    template = 'junkyard_app/components/base.html'
    wrapper_classnames = 'container'

    def __init__(
        self: Type,
        request: Type,
        wrapper_classnames: str = 'container'
    ) -> None:

        self.request = request
        self.wrapper_classnames = wrapper_classnames

    def get_context(
        self: Type
    ) -> dict:

        return {
            'request': self.request
        }

    def render(
        self: Type,
    ) -> str:

        return render_to_string(
            self.template,
            self.get_context(),
            request=self.request,
        )
