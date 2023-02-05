# -*- coding: utf-8 -*-
import os


class Settings:

    @property
    def API_HOSTNAME(self):
        return os.getenv('JUNKYARD_API_HOSTNAME', '')

    @property
    def COOKIE_NAME_SESSION_ID(self):
        return 'junkyard_app_sessionid'

    @property
    def URLNAME_CMS_HOME(self):
        return 'cms_home'

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
