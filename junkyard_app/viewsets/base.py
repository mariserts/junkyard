# -*- coding: utf-8 -*-
from typing import Type, Union

from django.core.signing import BadSignature, Signer
from django.views import View

from ..conf import settings


class BaseViewSet(View):

    def get_session_id_cookie(self):

        return self.request.COOKIES.get(
            settings.COOKIE_NAME_SESSION_ID,
            None
        )

    def get_token(
        self: Type,
    ) -> Union[None, str]:

        token = self.get_session_id_cookie()

        if token is None:
            return None

        try:
            return Signer().unsign_object(token)
        except BadSignature:
            return None

        return None

    def sign_token(
        self: Type,
        token: str,
    ) -> str:
        return Signer().sign_object(token)
