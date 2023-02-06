# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.core.signing import BadSignature, SignatureExpired
from django.shortcuts import redirect, reverse

from .conf import settings
from .signing import unsign


class UnAuthenticatedUserRequired(AccessMixin):

    def handle_has_token(self):
        return redirect(settings.URLNAME_CMS_HOME)

    def dispatch(self, request, *args, **kwargs):

        token = self.request.COOKIES.get(
            settings.COOKIE_NAME_SESSION_ID,
            None
        )

        if token is not None:
            return self.handle_has_token()

        return super().dispatch(request, *args, **kwargs)


class SessionTokenRequiredMixin(AccessMixin):

    def handle_no_token(self):
        messages.error(self.request, 'Authentication required!')
        url = reverse(settings.URLNAME_SIGN_IN)
        url += f'?next={self.request.path}'
        return redirect(url)

    def get_request_token(self):
        return getattr(
            self.request,
            settings.REQUEST_TOKEN_ATTR_NAME,
            {}
        )

    def get_api_token(self):
        data = self.get_request_token()
        return data.get('access_token', None)

    def get_api_user_id(self):
        data = self.get_request_token()
        return data.get('user', {}).get('id', None)

    def get_api_user_email(self):
        data = self.get_request_token()
        return data.get('user', {}).get('email', None)

    def dispatch(self, request, *args, **kwargs):

        token = self.request.COOKIES.get(
            settings.COOKIE_NAME_SESSION_ID,
            None
        )

        if token is None:
            return self.handle_no_token()

        try:
            data = unsign(token)

        except SignatureExpired:
            return self.handle_no_token()

        except BadSignature:
            return self.handle_no_token()

        setattr(
            request,
            settings.REQUEST_TOKEN_ATTR_NAME,
            data
        )

        return super().dispatch(request, *args, **kwargs)
