# -*- coding: utf-8 -*-
from django.conf import settings as dj_settings


class Settings:

    @property
    def CASCADE_TENANT_PERMISSIONS(self):
        return getattr(
            dj_settings,
            'JUNKYARD_API_CASCADE_TENANT_PERMISSIONS',
            True
        )

    @property
    def ITEM_TYPE_REGISTRY(self):
        return dj_settings._JUNKYARD_API_ITEM_TYPE_REGISTRY

    @property
    def LANGUAGE_ENGLISH(self):
        return ['en', 'English']

    @property
    def LANGUAGES(self):
        return [
            self.LANGUAGE_ENGLISH
        ]

    @property
    def LANGUAGE_DEFAULT(self):
        return self.LANGUAGE_ENGLISH[0]


settings = Settings()
