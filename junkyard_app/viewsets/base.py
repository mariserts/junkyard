# -*- coding: utf-8 -*-
from typing import Type

from django.views import View

from ..mixins import SessionTokenRequiredMixin, UnAuthenticatedUserRequired
from ..signing import sign


class BaseViewSet(View):

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
    pass


class UnAuthenticatedViewSet(
    UnAuthenticatedUserRequired,
    BaseViewSet
):
    pass
