from django.conf import settings as dj_settings


class Settings:

    @property
    def ITEM_TYPE_REGISTRY(self):
        return dj_settings._JUNKYARD_API_ITEM_TYPE_REGISTRY

    @property
    def CURRENCY_EUR(self):
        return ['eur', 'EUR']

    @property
    def CURRENCIES(self):
        return [
            self.CURRENCY_EUR
        ]

    @property
    def CURRENCIES_DEFAULT(self):
        return CURRENCY_EUR[0]

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
