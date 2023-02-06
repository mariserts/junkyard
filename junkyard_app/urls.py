# -*- coding: utf-8 -*-
from django.urls import path

from .conf import settings
from .viewsets.authenticate_register import RegisterViewSet
from .viewsets.authenticate_sign_in import SignInViewSet
from .viewsets.authenticate_sign_out import SignOutViewSet
from .viewsets.public_homepage import PublicHomePageViewSet
from .viewsets.cms_homepage import CmsHomePageViewSet

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
