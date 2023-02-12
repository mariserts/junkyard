# -*- coding: utf-8 -*-
from django.urls import path

from .conf import settings
from .viewsets.authenticate_register import RegisterViewSet
from .viewsets.authenticate_sign_in import SignInViewSet
from .viewsets.authenticate_sign_out import SignOutViewSet
from .viewsets.cms_homepage import CmsHomePageViewSet
from .viewsets.cms_project_homepage import CmsProjectHomePageViewSet
from .viewsets.cms_project_item import CmsProjectItemViewSet
from .viewsets.public_homepage import PublicHomePageViewSet


urlpatterns = [
    path(
        'cms/register/',
        RegisterViewSet.as_view(),
        name=settings.URLNAME_REGISTER
    ),
    path(
        'cms/sign-in/',
        SignInViewSet.as_view(),
        name=settings.URLNAME_SIGN_IN
    ),
    path(
        'cms/sign-out/',
        SignOutViewSet.as_view(),
        name=settings.URLNAME_SIGN_OUT
    ),
    path(
        'cms/projects/<int:project_pk>/items/<int:item_pk>/',
        CmsProjectItemViewSet.as_view(),
        name=settings.URLNAME_CMS_PROJECT_ITEM
    ),
    path(
        'cms/projects/<int:project_pk>/',
        CmsProjectHomePageViewSet.as_view(),
        name=settings.URLNAME_CMS_PROJECT_HOMEPAGE
    ),
    path(
        'cms/',
        CmsHomePageViewSet.as_view(),
        name=settings.URLNAME_CMS_HOMEPAGE
    ),
    path(
        '',
        PublicHomePageViewSet.as_view(),
        name=settings.URLNAME_PUBLIC_HOMEPAGE
    ),
]
