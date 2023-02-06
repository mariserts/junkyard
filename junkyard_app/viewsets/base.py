# -*- coding: utf-8 -*-
from typing import Type, Union

from django.shortcuts import HttpResponse
from django.views import View

from ..conf import settings
from ..mixins import SessionTokenRequiredMixin, UnAuthenticatedUserRequired
from ..signing import sign


class BaseViewSet(View):

    def sign_token(
        self: Type,
        token: str,
        max_age: int,
    ) -> str:
        return sign(token, max_age)

    def set_response_session_cookie(
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


class AuthenticatedViewSet(
    SessionTokenRequiredMixin,
    BaseViewSet
):
    pass


class UnAuthenticatedViewSet(
    UnAuthenticatedUserRequired,
    BaseViewSet
):
    pass
