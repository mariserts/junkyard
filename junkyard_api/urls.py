# -*- coding: utf-8 -*-
from django.urls import include, path, re_path

from rest_framework import permissions

from rest_framework_nested import routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .viewsets.public_items import PublicItemsViewSet
from .viewsets.tenant_admins import TenantAdminsViewSet
from .viewsets.tenant_items_item_relations import (
    TenantItemItemRelationsViewSet
)
from .viewsets.tenant_item_types import TenantItemTypesViewSet
from .viewsets.tenant_items import TenantItemsViewSet
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
    r'public-items',
    PublicItemsViewSet,
    basename='public-items'
)
router.register(
    r'users',
    UsersViewSet,
    basename='users'
)
router.register(
    r'tenants',
    TenantsViewSet,
    basename='tenants'
)


# tenant router
tenant_router = routers.NestedSimpleRouter(router, r'tenants', lookup='tenant')

# tenant nested urls
tenant_router.register(
    r'admins',
    TenantAdminsViewSet,
    basename='admins'
)
tenant_router.register(
    r'item-types',
    TenantItemTypesViewSet,
    basename='item_types'
)
tenant_router.register(
    r'items',
    TenantItemsViewSet,
    basename='items'
)


# Items router
items_router = routers.NestedSimpleRouter(
    tenant_router,
    r'items',
    lookup='item'
)

# Items nested urls
items_router.register(
    r'relations',
    TenantItemItemRelationsViewSet,
    basename='relations'
)


urlpatterns = [
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
        include(tenant_router.urls)
    ),
    path(
        'api/',
        include(items_router.urls)
    ),
]
