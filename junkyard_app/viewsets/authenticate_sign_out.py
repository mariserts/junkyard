# -*- coding: utf-8 -*-
from typing import Type
from django.contrib import messages
from django.http.request import HttpRequest
from django.shortcuts import HttpResponse, redirect

from ..conf import settings
from ..clients.authentication import AuthenticationClient
from ..clients.exceptions import UpStreamServerError, HTTPError

from .base import AuthenticatedViewSet


class SignOutViewSet(
    AuthenticatedViewSet
):

    def get(
        self: Type,
        request: HttpRequest,
    ) -> HttpResponse:

        access_token = self.get_api_token()

        error_response = redirect(settings.URLNAME_CMS_HOMEPAGE)

        try:
            AuthenticationClient().sign_out(access_token)

        except HTTPError:
            messages.success(
                request,
                'Signing out failed'
            )
            return error_response

        except UpStreamServerError:
            messages.warning(
                request,
                'UpStream server had issues'
            )
            return error_response

        messages.success(
            request,
            'See you next time'
        )

        response = redirect(settings.URLNAME_SIGN_IN)

        self.set_session_cookie(response, {}, -999999)

        return response
