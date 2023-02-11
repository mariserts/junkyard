# -*- coding: utf-8 -*-
from collections import OrderedDict
from typing import Type

from django.conf import settings as dj_settings


class LanguageRegistry:

    languages = OrderedDict()

    def __init__(
        self: Type
    ) -> None:

        for language in dj_settings.LANGUAGES:
            self.register(language[0], language[1])

    def register(
        self: Type,
        code: str,
        name: str
    ) -> None:

        self.languages[code] = name
