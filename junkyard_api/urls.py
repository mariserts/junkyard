# -*- coding: utf-8 -*-
from django.urls import include, path, re_path

from rest_framework import permissions

from rest_framework_nested import routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .conf import settings
from .viewsets.items import ItemsViewSet
from .viewsets.public_items import PublicItemsViewSet
from .viewsets.tenants import TenantsViewSet
from .viewsets.users import UsersViewSet


schema_view = get_schema_view(
    openapi.Info(
        title='Junkyard API',
        default_version='v1',
        description='Junkyard API docs',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='contact@snippets.local'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


router = routers.SimpleRouter()
router.register(r'items', ItemsViewSet, basename='items')
router.register(r'public-items', PublicItemsViewSet, basename='public-items')
router.register(r'tenants', TenantsViewSet, basename='tenants')
router.register(r'users', UsersViewSet, basename='users')


specific_type_router = routers.SimpleRouter()

for item_type in settings.ITEM_TYPE_REGISTRY.get_types_as_list():
    specific_type_router.register(
        rf'{item_type.name}',
        item_type.viewset,
        basename=f'{item_type.name}-items'
    )


urlpatterns = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    re_path(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
    path(
        'api/',
        include(router.urls)
    ),
    path(
        'api/items/',
        include(specific_type_router.urls)
    ),
]
