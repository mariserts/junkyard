# -*- coding: utf-8 -*-
from typing import Type

from django.contrib import messages
from django.http.request import HttpRequest
from django.shortcuts import HttpResponse, redirect, render, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

from ..conf import settings
from ..clients.authentication import AuthenticationClient
from ..clients.exceptions import (
    ClientRequestError,
    UpStreamServerError,
    HTTPError
)
from ..forms.register import RegisterForm

from .base import UnAuthenticatedViewSet


class RegisterViewSet(
    UnAuthenticatedViewSet
):

    template = 'junkyard_app/pages/authentication.html'

    def get_context(
        self: Type
    ):

        form = RegisterForm()
        if self.request.method == 'POST':
            form = RegisterForm(data=self.request.POST)

        return {
            'page': {
                'title': 'Authentication',
                'subtitle': 'Register'
            },
            'form': {
                'action': reverse(settings.URLNAME_REGISTER),
                'button_text': 'Register',
                'enctype': None,
                'form': form,
                'method': 'POST',
            },
            'links': [
                {
                    'text': 'Sign in',
                    'link': reverse(settings.URLNAME_SIGN_IN)
                },
                {
                    'text': 'Forgot password',
                    'link': '#'
                },
            ]
        }

    def get(
        self: Type,
        request: HttpRequest,
    ) -> HttpResponse:
        return render(
            request,
            self.template,
            context=self.get_context()
        )

    @method_decorator(sensitive_post_parameters([
        'password',
        'repeat_password'
    ]))
    def post(
        self: Type,
        request: HttpRequest,
    ) -> HttpResponse:

        context = self.get_context()
        form = context['form']['form']

        if form.is_valid() is False:
            messages.error(
                request,
                'Invalid form data'
            )
            return render(
                request,
                self.template,
                context=context,
                status=400
            )

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        repeat_password = form.cleaned_data['repeat_password']

        error_url = reverse(settings.URLNAME_REGISTER)
        error_url += f'?email={email}'

        error_response = redirect(error_url)

        if password != repeat_password:
            messages.error(
                request,
                'Passwords do not match'
            )
            return error_response

        try:
            data = AuthenticationClient().register(email, password)

        except ClientRequestError as error:
            messages.error(
                request,
                error
            )
            return error_response

        except HTTPError as error:
            messages.error(
                request,
                error
            )
            return error_response

        except UpStreamServerError:
            messages.error(
                request,
                'UpStream server had issues'
            )
            return error_response

        response = redirect(settings.URLNAME_CMS_HOME)

        self.set_response_session_cookie(
            response,
            {
                'access_token': data['access_token'],
                'user': data['user'],
            },
            data['expires_in']
        )

        return response
