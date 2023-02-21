# -*- coding: utf-8 -*-
from django.apps import AppConfig


class JunkyardApiPartCategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'junkyard_api_part_category'

    def ready(self):

        from junkyard_api.conf import settings as junkyard_api_settings

        from .registry_entry import PartCategoryRegistryEntry

        junkyard_api_settings.ITEM_TYPE_REGISTRY.register(
            PartCategoryRegistryEntry)
