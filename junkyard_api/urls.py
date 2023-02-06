# -*- coding: utf-8 -*-
from django.urls import include, path, re_path

from rest_framework import permissions

from rest_framework_nested import routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .conf import settings

from .viewsets.admins import AdminsViewSet
from .viewsets.authenticate import AuthenticationViewSet
from .viewsets.item_types import ItemTypesViewSet
from .viewsets.item_relations import ItemRelationsViewSet
from .viewsets.items import ItemsViewSet
from .viewsets.languages import LanguagesViewSet
from .viewsets.signing import SigningViewSet
from .viewsets.tenants import TenantsViewSet
from .viewsets.users import UsersViewSet


# drf yasg
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


#
router = routers.SimpleRouter()


# Base urls
router.register(
    r'admins',
    AdminsViewSet,
    basename='admins'
)
router.register(
    settings.PATH_AUTHENTICATE,
    AuthenticationViewSet,
    basename=settings.BASENAME_AUTHENTICATE
)
router.register(
    r'item-types',
    ItemTypesViewSet,
    basename='item-types'
)
router.register(
    r'items',
    ItemsViewSet,
    basename='items'
)
router.register(
    r'languages',
    LanguagesViewSet,
    basename='languages'
)
router.register(
    r'signer',
    SigningViewSet,
    basename='signer'
)
router.register(
    r'tenants',
    TenantsViewSet,
    basename='tenants'
)
router.register(
    r'users',
    UsersViewSet,
    basename='users'
)


# tenant router
items_router = routers.NestedSimpleRouter(
    router,
    r'items',
    lookup='item'
)
items_router.register(
    r'relations',
    ItemRelationsViewSet,
    basename='relations'
)


urlpatterns = [
    path(
        'accounts/',
        include('django.contrib.auth.urls')
    ),
    path(
        'o/',
        include('oauth2_provider.urls', namespace='oauth2_provider')
    ),
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
        'api/',
        include(items_router.urls)
    ),
]
