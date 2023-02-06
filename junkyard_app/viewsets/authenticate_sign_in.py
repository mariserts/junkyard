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
from ..forms.sign_in import SignInForm
from ..signing import sign

from .base import UnAuthenticatedViewSet


class SignInViewSet(
    UnAuthenticatedViewSet
):

    template = 'junkyard_app/pages/authentication.html'

    def get_context(
        self: Type
    ):

        if self.request.method == 'POST':
            form = SignInForm(data=self.request.POST)
        else:
            form = SignInForm(None, initial=self.request.GET)

        return {
            'page': {
                'title': 'Authentication',
                'subtitle': 'Sign in'
            },
            'form': {
                'action': reverse(settings.URLNAME_SIGN_IN),
                'button_text': 'Sign in',
                'enctype': None,
                'form': form,
                'method': 'POST',
            },
            'links': [
                {
                    'text': 'Register',
                    'link': reverse(settings.URLNAME_REGISTER)
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

    @method_decorator(sensitive_post_parameters(['password']))
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
        next = form.cleaned_data.get('next', None)

        error_url = reverse(settings.URLNAME_SIGN_IN)
        error_url += f'?email={email}'

        if next not in [None, '']:
            error_url += f'&next={next}'

        error_response = redirect(error_url)

        try:
            data = AuthenticationClient().sign_in(email, password)

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

        redirect_to = settings.URLNAME_CMS_HOME
        if next not in [None, '']:
            redirect_to = next

        response = redirect(redirect_to)

        response.set_cookie(
            settings.COOKIE_NAME_SESSION_ID,
            sign(
                {
                    'access_token': data['access_token'],
                    'user': data['user'],
                },
                max_age=data['expires_in']
            ),
            max_age=data['expires_in']
        )

        return response
