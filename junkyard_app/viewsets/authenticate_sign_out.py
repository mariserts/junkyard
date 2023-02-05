# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http.request import HttpRequest
from django.shortcuts import HttpResponse, redirect

from ..conf import settings
from ..clients.authentication import AuthenticationClient
from ..clients.exceptions import UpStreamServerError, HTTPError

from .base import BaseViewSet


class SignOutViewSet(BaseViewSet):

    def get(
        self: BaseViewSet,
        request: HttpRequest,
    ) -> HttpResponse:

        token = self.get_token()

        error_response = redirect(settings.URLNAME_CMS_HOME)

        if token is None:
            return HttpResponse(
                'Forbidden, no session cookie',
                status=403
            )

        try:
            AuthenticationClient().sign_out(token)

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

        response.set_cookie(
            settings.COOKIE_NAME_SESSION_ID,
            '',
            max_age=-99999
        )

        return response
