# -*- coding: utf-8 -*-
from typing import Type

import requests

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.core.signing import BadSignature, SignatureExpired
from django.core.validators import validate_email
from django.db.models.query import QuerySet

from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse

from oauth2_provider.models import AccessToken

from ..conf import settings
from ..models import Application, User
from ..serializers.authenticate import (
    BaseSerializer,
    EmailSerializer,
    EmailPasswordSerializer,
    EmailTokenPasswordSerializer,
    PasswordSerializer,
    TokenSerializer,
)
from ..cryptography.exceptions import (
    BadMaxAgeException,
    BadSignatureFormatException
)
from ..cryptography.sign import sign_object
from ..cryptography.unsign import unsign_object

from oauth2_provider.contrib.rest_framework import OAuth2Authentication


class AuthenticationViewSet(
    viewsets.GenericViewSet
):

    PATH_GET_PASSWORD_RESET_LINK = 'get-password-reset-link'
    PATH_REGISTER = 'register'
    PATH_SET_PASSWORD = 'set-password'
    PATH_SET_PASSWORD_TOKEN = 'set-password-with-token'
    PATH_SIGN_IN = 'sign-in'
    PATH_SIGN_OUT = 'sign-out'
    PATH_TERMINATE_ACCOUNT = 'teminate'

    authentication_classes = (OAuth2Authentication, )
    queryset = QuerySet()

    def get_serializer_class(
        self: Type,
    ) -> serializers.Serializer:

        if self.action in ['register', 'sign_in']:
            return EmailPasswordSerializer

        if self.action == 'sign_out':
            return TokenSerializer

        if self.action == 'set_password':
            return PasswordSerializer

        if self.action == 'set_password_with_token':
            return EmailTokenPasswordSerializer

        if self.action == 'get_password_reset_link':
            return EmailSerializer

        return BaseSerializer

    @action(
        detail=False,
        methods=['POST'],
        name='Register',
        url_path=PATH_REGISTER,
    )
    @permission_classes([permissions.AllowAny, ])
    def register(
        self: Type,
        request: Request
    ) -> Response:

        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid() is False:
            return Response(
                serializer.errors,
                status=400
            )

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError({
                'email': ['Email is invalid']
            })

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({
                'password': [str(e)]
            })

        if User.objects.filter(email=email).exists():
            return Response(
                'Email is taken',
                status=400
            )

        user = User.objects.create(email=email, is_active=True)
        user.set_password(password)
        user.save()

        request = requests.post(
            f'{self.get_full_request_hostname()}/o/token/',
            json={
                'grant_type': Application.GRANT_PASSWORD,
                'username': email,
                'password': password,
                'client_id': settings.API_CLIENT_ID,
                'client_secret': settings.API_CLIENT_SECRET,
            },
            headers={
                'content-type': 'application/json',
            },
        )

        if request.ok is True:

            response_data = request.json()
            response_data['user'] = {
                'id': user.id,
                'email': user.email
            }

            return Response(
                response_data,
                status=201
            )

        return Response(
            request.json(),
            status=request.status_code,
        )

    @action(
        detail=False,
        methods=['POST'],
        name='Sign in',
        url_path=PATH_SIGN_IN,
    )
    @permission_classes([permissions.AllowAny, ])
    def sign_in(
        self: Type,
        request: Request
    ) -> Response:

        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid() is False:
            return Response(
                serializer.errors,
                status=400
            )

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = self.get_user_for_email_and_password(email, password)
        if user is None:
            return Response(
                'Invalid credentials',
                status=400
            )

        if user.is_active is False:
            return Response(
                'User is not active',
                status=404
            )

        request = requests.post(
            f'{self.get_full_request_hostname()}/o/token/',
            json={
                'grant_type': Application.GRANT_PASSWORD,
                'username': email,
                'password': password,
                'client_id': settings.API_CLIENT_ID,
                'client_secret': settings.API_CLIENT_SECRET,
            },
            headers={
                'content-type': 'application/json',
            },
        )

        if request.ok is True:

            response_data = request.json()
            response_data['user'] = {
                'id': user.id,
                'email': user.email,
            }

            return Response(
                response_data,
                status=201
            )

        return Response(
            request.json(),
            status=request.status_code,
        )

    @action(
        detail=False,
        methods=['POST'],
        name='Sign out',
        url_path=PATH_SIGN_OUT,
    )
    @permission_classes((permissions.IsAuthenticated))
    def sign_out(
        self: Type,
        request: Request
    ) -> Response:

        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid() is False:
            return Response(
                serializer.errors,
                status=400
            )

        token = serializer.validated_data['token']

        try:
            user = self.get_user_for_token(token)
        except AccessToken.DoesNotExist:
            return Response(
                'Token does not exist',
                status=404
            )

        if user != request.user:
            return Response(
                'Can not sign out other users',
                status=403
            )

        request = requests.post(
            f'{self.get_full_request_hostname()}/o/revoke_token/',
            json={
                'token': token,
                'client_id': settings.API_CLIENT_ID,
                'client_secret': settings.API_CLIENT_SECRET,
            },
        )

        if request.ok is True:
            return Response(
                {'message': 'token revoked'},
                request.status_code
            )

        return Response(
            request.json(),
            status=request.status_code,
            content_type='application/json',
        )

    @action(
        detail=False,
        methods=['POST'],
        name='Change password',
        url_path=PATH_SET_PASSWORD,
    )
    @permission_classes([permissions.IsAuthenticated, ])
    def set_password(
        self: Type,
        request: Request
    ) -> Response:

        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid() is False:
            return Response(
                serializer.errors,
                status=400
            )

        password = serializer.validated_data['password']

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({'password': str(e)})

        request.user.set_password(password)

        return Response(
            {},
            status=200
        )

    @action(
        detail=False,
        methods=['POST'],
        name='Change password with token',
        url_path=PATH_SET_PASSWORD_TOKEN,
    )
    @permission_classes([permissions.AllowAny, ])
    def set_password_with_token(
        self: Type,
        request: Request
    ) -> Response:

        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid() is False:
            return Response(
                serializer.errors,
                status=400
            )

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        token = serializer.validated_data['token']

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({
                'password': [str(e)]
            })

        try:
            unsigned_data = unsign_object(token)

        except BadSignatureFormatException:
            raise serializers.ValidationError({
                'token': ['Bad token format']
            })

        except BadMaxAgeException:
            return Response(
                {'message': 'Bad token max age'},
                status=400
            )

        except SignatureExpired:
            return Response(
                {'message': 'Token expired'},
                status=400
            )

        except BadSignature:
            return Response(
                {'message': 'Token has been tampered with'},
                status=400
            )

        unsigned_email = unsigned_data.get('email', None)
        unsigned_action = unsigned_data.get('action', None)

        if unsigned_action != 'set_password':
            return Response(
                {'message': 'Bad token data'},
                status=400
            )

        if unsigned_email != email:
            return Response(
                {'message': 'Bad token data'},
                status=400
            )

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response(
                f'User with "{email}" does not exist',
                status=404
            )

        user.set_password(password)
        user.save()

        return Response(
            {'message': 'Password changed'},
            status=200
        )

    @action(
        detail=False,
        methods=['POST'],
        name='request password reset link',
        url_path=PATH_GET_PASSWORD_RESET_LINK,
    )
    @permission_classes([permissions.AllowAny, ])
    def get_password_reset_link(
        self: Type,
        request: Request
    ) -> Response:

        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid() is False:
            return Response(
                serializer.errors,
                status=400
            )

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist():
            return Response(
                {'message': f'User with email "{email}" does not exist'},
                status=404
            )

        data = {
            'email': user.email,
            'action': 'set_password',
        }

        signed_data = sign_object(
            data=data,
            max_age=30*60
        )

        url = self.get_full_request_hostname()
        url += reverse(
            f'{settings.BASENAME_AUTHENTICATE}-{self.PATH_SET_PASSWORD_TOKEN}',
            request=request
        )

        token = signed_data['signature']
        link = f'{url}?email={user.email}&token={token}'

        # XXXX TODO FIX
        try:
            self.send_link(user.email, link)
        except Exception:
            return Response(
                {'message': 'Something failed'},
                status=500
            )

        return Response(
            {},
            status=201
        )

    @action(
        detail=False,
        methods=['DELETE'],
        name='terminate account',
        url_path=PATH_TERMINATE_ACCOUNT,
    )
    @permission_classes([permissions.IsAuthenticated, ])
    def terminate_account(
        self: Type,
        request: Request
    ) -> Response:

        #
        self.request.user.delete()

        return Response(
            {},
            status=200
        )

    def send_link(
        self: Type,
        email: str,
        link: str,
    ) -> None:

        subject = 'Password reset link request from JunkyardApi'
        from_email = 'from@example.com'
        text_content = f'Follow link: {link}'
        html_content = f'<p>Follow link: <a href="{link}">{link}</a>"</p>'

        msg = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            [email]
        )
        msg.attach_alternative(
            html_content,
            'text/html'
        )
        msg.send()

    def get_full_request_hostname(
        self: Type,
    ) -> str:
        hostname = 'http'
        if self.request.is_secure is True:
            hostname += 's'
        hostname += '://'
        hostname += self.request.get_host()
        return hostname

    def get_user_for_token(
        self: Type,
        token: str,
    ) -> User:

        access_token = AccessToken.objects.filter(
            token=token
        ).select_related(
            'application'
        ).first()

        if access_token is None:
            raise AccessToken.DoesNotExist()

        if access_token.user is None:
            return access_token.application.user

        return access_token.user

    def get_user_for_email_and_password(
        self: Type,
        email: str,
        password: str,
    ) -> User:

        user = authenticate(username=email, password=password)
        if user is None:
            raise User.DoesNotExist()

        return user
