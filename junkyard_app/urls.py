# -*- coding: utf-8 -*-
from django.urls import path

from .conf import settings
from .viewsets.authenticate_register import RegisterViewSet
from .viewsets.authenticate_sign_in import SignInViewSet
from .viewsets.authenticate_sign_out import SignOutViewSet
from .viewsets.cms_home import CmsHomeViewSet

urlpatterns = [
    path(
        'register/',
        RegisterViewSet.as_view(),
        name=settings.URLNAME_REGISTER
    ),
    path(
        'sign-in/',
        SignInViewSet.as_view(),
        name=settings.URLNAME_SIGN_IN
    ),
    path(
        'sign-out/',
        SignOutViewSet.as_view(),
        name=settings.URLNAME_SIGN_OUT
    ),
    path(
        'cms/',
        CmsHomeViewSet.as_view(),
        name=settings.URLNAME_CMS_HOME
    ),
]
