# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.core.signing import BadSignature, SignatureExpired
from django.shortcuts import redirect, reverse

from .clients.users import UsersClient
from .conf import settings
from .signing import unsign


class SessionTokenMixin:

    def get_session_cookie(self):
        return self.request.COOKIES.get(
            settings.COOKIE_NAME_SESSION_ID,
            None
        )

    def get_request_token_data(self):
        return getattr(
            self.request,
            settings.REQUEST_TOKEN_ATTR_NAME,
            {}
        )

    def get_api_token(self):
        data = self.get_request_token_data()
        return data.get('access_token', None)

    def get_api_user(self):
        data = self.get_request_token_data()
        return data.get('user', None)

    def get_api_user_id(self):
        data = self.get_request_token_data()
        return data.get('user', {}).get('id', None)

    def get_api_user_email(self):
        data = self.get_request_token_data()
        return data.get('user', {}).get('email', None)

    def is_authenticated(self):
        return self.get_session_cookie() is not None

    def set_request_token_data(self, data):

        if data is None:
            return None

        user = data.get('user', None)
        access_token = data.get('access_token', None)

        if user is None:
            return None

        if access_token is None:
            return None

        # XXXX Cache
        # Cache key f'SessionTokenMixin.set_request_token_data__{access_token}'
        # Cache timeout 10s-30s

        response = UsersClient().get_user(
            access_token,
            data['user']['id']
        )

        data['user'] = response

        setattr(
            self.request,
            settings.REQUEST_TOKEN_ATTR_NAME,
            data
        )


class PublicSiteAccessMixin(
    SessionTokenMixin,
    AccessMixin
):

    def dispatch(self, request, *args, **kwargs):

        data = {
            'access_token': None,
            'user': None
        }
        token = self.get_session_cookie()

        if token is not None:

            try:
                data = unsign(token)

            except SignatureExpired:
                pass

            except BadSignature:
                pass

        self.set_request_token_data(data)

        return super().dispatch(request, *args, **kwargs)


class UnAuthenticatedUserRequired(AccessMixin):

    def handle_has_token(self):
        return redirect(settings.URLNAME_CMS_HOMEPAGE)

    def dispatch(self, request, *args, **kwargs):

        token = self.get_session_cookie()

        if token is not None:
            return self.handle_has_token()

        return super().dispatch(request, *args, **kwargs)


class SessionTokenRequiredMixin(
    SessionTokenMixin,
    AccessMixin
):

    def handle_no_token(self):
        messages.error(self.request, 'Authentication required!')
        url = reverse(settings.URLNAME_SIGN_IN)
        url += f'?next={self.request.path}'
        return redirect(url)

    def dispatch(self, request, *args, **kwargs):

        token = self.get_session_cookie()

        if token is None:
            return self.handle_no_token()

        try:
            data = unsign(token)

        except SignatureExpired:
            return self.handle_no_token()

        except BadSignature:
            return self.handle_no_token()

        self.set_request_token_data(data)

        return super().dispatch(request, *args, **kwargs)
