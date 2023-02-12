# -*- coding: utf-8 -*-
from typing import Type

from django.template.loader import render_to_string


class BaseComponent:

    request = None
    template = 'junkyard_app/components/base.html'

    def __init__(
        self: Type,
        request: Type,
    ) -> None:

        self.request = request

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

    def __repr__(
        self: Type
    ) -> str:

        return self.render()
