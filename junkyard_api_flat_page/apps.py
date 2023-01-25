from django.apps import AppConfig


class JunkyardApiFlatPageConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'junkyard_api_flat_page'

    def ready(self):

        from junkyard_api.conf import settings as junkyard_api_settings

        from .conf import settings
        from .serializers import FlatPageSerializer

        junkyard_api_settings.ITEM_TYPE_REGISTRY.register(
            settings.ITEM_TYPE,
            FlatPageSerializer
        )
