# -*- coding: utf-8 -*-
from typing import Type

from .base import BaseComponent


class HeadingH1Component(
    BaseComponent
):

    template = 'junkyard_app/components/heading_h1_jumbo.html'
    text = None
    wrapper_classnames = ''

    def __init__(
        self: Type,
        request: Type,
        text: str = '',
        subtitle: str = '',
    ) -> None:

        self.request = request
        self.subtitle = subtitle
        self.text = text

    def get_context(
        self: Type
    ) -> dict:

        context = super().get_context()

        context['subtitle'] = self.subtitle
        context['text'] = self.text

        return context
