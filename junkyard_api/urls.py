# -*- coding: utf-8 -*-
from django.urls import include, path, re_path

from rest_framework import permissions

from rest_framework_nested import routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .conf import settings

# from .viewsets.item_types import ItemTypesViewSet
# from .viewsets.item_relations import ItemRelationsViewSet
# from .viewsets.items import ItemsViewSet
# from .viewsets.languages import LanguagesViewSet
# from .viewsets.signing import SigningViewSet
# from .viewsets.tenants import TenantsViewSet
# from .viewsets.users import UsersViewSet

from .viewsets.authenticate import AuthenticationViewSet
from .viewsets.languages import LanguagesViewSet
from .viewsets.projects_languages import ProjectsLanguagesViewSet
from .viewsets.projects_item_types import ProjectsItemTypesViewSet
from .viewsets.projects_items import ProjectsItemsViewSet
from .viewsets.projects_tenants_items import ProjectsTenantsItemsViewSet
from .viewsets.projects_tenants_users import ProjectsTenantsUsersViewSet
from .viewsets.projects_tenants import ProjectsTenantsViewSet
from .viewsets.projects_users import ProjectsUsersViewSet
from .viewsets.projects import ProjectsViewSet
from .viewsets.signing import SigningViewSet
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
    permission_classes=[
        permissions.AllowAny
    ],
)

#
router = routers.SimpleRouter()

# Base urls
# /api/
router.register(settings.PATH_AUTHENTICATE, AuthenticationViewSet,basename=settings.BASENAME_AUTHENTICATE)
router.register(r'projects', ProjectsViewSet, basename='projects')
# router.register(r'languages', LanguagesViewSet, basename='languages')
router.register(r'cryptography', SigningViewSet, basename='cryptography')
router.register(r'users', UsersViewSet, basename='users')

# /api/projects/
projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register(r'item-types', ProjectsItemTypesViewSet, basename='item-types')
projects_router.register(r'items', ProjectsItemsViewSet, basename='items')
projects_router.register(r'languages', ProjectsLanguagesViewSet, basename='languages')
projects_router.register(r'tenants', ProjectsTenantsViewSet, basename='tenants')
projects_router.register(r'users', ProjectsUsersViewSet, basename='users')

# /api/projects/<project_pk>/
tenant_router = routers.NestedSimpleRouter(projects_router, r'tenants', lookup='tenant')
tenant_router.register(r'items', ProjectsTenantsItemsViewSet, basename='items')
tenant_router.register(r'users', ProjectsTenantsUsersViewSet, basename='users')


urlpatterns = [
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',schema_view.without_ui(cache_timeout=0),name='schema-json'),
    re_path(r'^swagger/$',schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    re_path(r'^redoc/$',schema_view.with_ui('redoc', cache_timeout=0),name='schema-redoc'),
    path('api/', include(router.urls)),
    path('api/', include(projects_router.urls)),
    path('api/', include(tenant_router.urls)),
]
