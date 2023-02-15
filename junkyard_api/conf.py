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
    def BASENAME_PROJECTS_ITEMS(self):
        return 'projects-items'

    @property
    def BASENAME_PROJECTS_TENANTS_ITEMS(self):
        return 'projects-tenants-items'

    @property
    def CASCADE_TENANT_PERMISSIONS(self):
        return os.getenv('CASCADE_TENANT_PERMISSIONS') in TRUE

    @property
    def ITEM_TYPE_REGISTRY(self):
        return dj_settings._JUNKYARD_API_ITEM_TYPE_REGISTRY

    @property
    def LANGUAGES_REGISTRY(self):
        return dj_settings._JUNKYARD_API_LANGUAGES_REGISTRY

    @property
    def PATH_AUTHENTICATE(self):
        return r'authenticate'


settings = Settings()
