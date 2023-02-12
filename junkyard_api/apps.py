# -*- coding: utf-8 -*-
from django.apps import AppConfig


class JunkyardApiConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'junkyard_api'

    def ready(self):

        from django.conf import settings as dj_settings

        from .item_types.registry import ItemTypeRegistry
        from .languages.registry import LanguageRegistry

        dj_settings._JUNKYARD_API_ITEM_TYPE_REGISTRY = ItemTypeRegistry()
        dj_settings._JUNKYARD_API_LANGUAGES_REGISTRY = LanguageRegistry()
