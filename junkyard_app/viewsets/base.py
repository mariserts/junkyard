# -*- coding: utf-8 -*-
from typing import Type, Union

from django.shortcuts import HttpResponse
from django.views import View

from ..conf import settings
from ..mixins import (
    PublicSiteAccessMixin,
    SessionTokenRequiredMixin,
    UnAuthenticatedUserRequired
)
from ..signing import sign


class BaseViewSet(View):

    def get_context(self):
        return {
            'user': None
        }

    def get_session_cookie(self):
        return self.request.COOKIES.get(
            settings.COOKIE_NAME_SESSION_ID,
            None
        )

    def is_authenticated(self):
        return self.get_session_cookie() is not None

    def set_session_cookie(
        self: Type,
        response: HttpResponse,
        data: Union[str, int, dict],
        max_age: int
    ) -> None:

        response.set_cookie(
            settings.COOKIE_NAME_SESSION_ID,
            sign(data, max_age),
            max_age=max_age
        )

    def sign_token(
        self: Type,
        token: str,
        max_age: int,
    ) -> str:
        return sign(token, max_age)


class AuthenticatedViewSet(
    SessionTokenRequiredMixin,
    BaseViewSet
):

    def get_context(self):
        context = super().get_context()
        context = {'user': self.get_api_user()}
        return context


class PublicSiteViewSet(
    PublicSiteAccessMixin,
    BaseViewSet
):
    def get_context(self):
        context = super().get_context()
        context = {'user': self.get_api_user()}
        return context


class UnAuthenticatedViewSet(
    UnAuthenticatedUserRequired,
    BaseViewSet
):
    pass
