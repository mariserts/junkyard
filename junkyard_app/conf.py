# -*- coding: utf-8 -*-
import os


class Settings:

    #
    # API variable
    #

    @property
    def API_HOSTNAME(self):
        return os.getenv(
            'JUNKYARD_API_HOSTNAME',
            'http://0.0.0.0:8000'
        )

    #
    # Coocie names
    #

    @property
    def COOKIE_NAME_SESSION_ID(self):
        return os.getenv(
            'JUNKYARD_SESSION_COOKIE_NAME',
            'junkyard_app_sessionid'
        )

    #
    # Request attributes
    #

    @property
    def REQUEST_TOKEN_ATTR_NAME(self):
        return os.getenv(
            'JUNKYARD_REQUEST_TOKEN_NAME',
            'junkyard_token'
        )

    #
    #
    #

    @property
    def TEXT_PROJECT_TITLE(self):
        return os.getenv(
            'JUNKYARD_PROJECT_TITLE',
            'JunkyardApp'
        )

    #
    # Url names
    #

    @property
    def URLNAME_CMS_HOMEPAGE(self):
        return 'cms_homepage'

    @property
    def URLNAME_PUBLIC_HOMEPAGE(self):
        return 'public_homepage'

    @property
    def URLNAME_REGISTER(self):
        return 'register'

    @property
    def URLNAME_SIGN_IN(self):
        return 'sign_in'

    @property
    def URLNAME_SIGN_OUT(self):
        return 'sign_out'


settings = Settings()
