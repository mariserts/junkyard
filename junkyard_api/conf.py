# -*- coding: utf-8 -*-
import os

from django.conf import settings as dj_settings


TRUE = ['true', 'True', 1, '1', True]


class Settings:

    @property
    def API_CLIENT_ID(self):
        return os.getenv('API_CLIENT_ID')

    @property
    def API_CLIENT_SECRET(self):
        return os.getenv('API_CLIENT_SECRET')

    @property
    def BASENAME_AUTHENTICATE(self):
        return 'authenticate'

    @property
    def CASCADE_TENANT_PERMISSIONS(self):
        return os.getenv('CASCADE_TENANT_PERMISSIONS') in TRUE

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

    @property
    def PATH_AUTHENTICATE(self):
        return r'authenticate'


settings = Settings()
