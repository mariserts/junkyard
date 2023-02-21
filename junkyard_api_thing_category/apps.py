# -*- coding: utf-8 -*-
from django.apps import AppConfig


class JunkyardApiThingCategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'junkyard_api_thing_category'

    def ready(self):

        from junkyard_api.conf import settings as junkyard_api_settings

        from .registry_entry import ThingCategoryRegistryEntry

        junkyard_api_settings.ITEM_TYPE_REGISTRY.register(
            ThingCategoryRegistryEntry)
