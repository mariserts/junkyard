# -*- coding: utf-8 -*-
from typing import List

import requests

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.core.signing import BadSignature, SignatureExpired
from django.core.validators import validate_email
from django.db.models.query import QuerySet
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

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
from ..signers.exceptions import (
    BadMaxAgeException,
    BadSignatureFormatException
)
from ..signers.sign import sign_object
from ..signers.unsign import unsign_object


class AuthenticationViewSet(viewsets.GenericViewSet):

    PATH_GET_PASSWORD_RESET_LINK = 'get-password-reset-link'
    PATH_REGISTER = 'register'
    PATH_SET_PASSWORD = 'set-password'
    PATH_SET_PASSWORD_TOKEN = 'set-password-with-token'
    PATH_SIGN_IN = 'sign-in'
    PATH_SIGN_OUT = 'sign-out'

    queryset = QuerySet()

    def get_serializer_class(
        self: viewsets.GenericViewSet,
    ) -> serializers.Serializer:

        if self.action in ['register', 'sign_in']:
            return EmailPasswordSerializer

        if self.action in ['sign_out', ]:
            return TokenSerializer

        if self.action in 'set_password':
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
    # @method_decorator(sensitive_post_parameters('password'))
    @permission_classes([permissions.AllowAny, ])
    def register(
        self: viewsets.GenericViewSet,
        request: Request
    ) -> Response:

        serializer = EmailPasswordSerializer(data=request.data)
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

        try:
            credentials = self.get_credentials_for_user_id(user.id)
        except Application.DoesNotExist:
            return Response(
                'User does not have application',
                status=404
            )

        request = requests.post(
            f'{self.get_full_request_hostname()}/o/token/',
            json={
                'grant_type': 'client_credentials',
                'client_id': credentials[0],
                'client_secret': credentials[1],
            },
            headers={
                'content-type': 'application/json',
            },
        )

        if request.ok is True:
            return Response(
                request.json(),
                status=201
            )

        return Response(
            request.json(),
            status=request.status_code,
            content_type='application/json',
        )

    @action(
        detail=False,
        methods=['POST'],
        name='Sign in',
        url_path=PATH_SIGN_IN,
    )
    # @method_decorator(sensitive_post_parameters('password'))
    @permission_classes([permissions.AllowAny, ])
    def sign_in(
        self: viewsets.GenericViewSet,
        request: Request
    ) -> Response:

        serializer = EmailPasswordSerializer(data=request.data)
        if serializer.is_valid() is False:
            return Response(
                serializer.errors,
                status=400
            )

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = self.get_user_for_email_and_password(email, password)
        except User.DoesNotExist:
            return Response(
                'User credentials are incorrect',
                status=404
            )

        try:
            credentials = self.get_credentials_for_user_id(user.id)
        except Application.DoesNotExist:
            return Response(
                'User does not have application',
                status=404
            )

        request = requests.post(
            f'{self.get_full_request_hostname()}/o/token/',
            json={
                'grant_type': 'client_credentials',
                'client_id': credentials[0],
                'client_secret': credentials[1],
            },
            headers={
                'content-type': 'application/json',
            },
        )

        if request.ok is True:
            return Response(
                request.json(),
                status=200
            )

        return Response(
            request.json(),
            status=request.status_code,
            content_type='application/json'
        )

    @action(
        detail=False,
        methods=['POST'],
        name='Sign out',
        url_path=PATH_SIGN_OUT,
    )
    @permission_classes([permissions.AllowAny, ])
    def sign_out(
        self: viewsets.GenericViewSet,
        request: Request
    ) -> Response:

        try:
            token = request.data['token']
        except KeyError:
            raise serializers.ValidationError({
                'token': ['"token" is required']
            })

        try:
            user = self.get_user_for_token(token)
        except AccessToken.DoesNotExist:
            return Response(
                'Token doe not exist',
                status=404
            )

        if user != request.user:
            return Response(
                'Can not sign out other users',
                status=403
            )

        credentials = self.get_credentials_for_user_id(user.id)

        request = requests.post(
            f'{self.get_full_request_hostname()}/o/revoke_token/',
            json={
                'token': token,
                'client_id': credentials[0],
                'client_secret': credentials[1],
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
    # @method_decorator(sensitive_post_parameters('password'))
    @permission_classes([permissions.IsAuthenticated, ])
    def set_password(
        self: viewsets.GenericViewSet,
        request: Request
    ) -> Response:

        try:
            password = request.data['password']
        except KeyError:
            raise serializers.ValidationError({
                'password': ['"password" is required']
            })

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({
                'password': [str(e)]
            })

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
    @method_decorator(sensitive_post_parameters('password'))
    @permission_classes([permissions.AllowAny, ])
    def set_password_with_token(
        self: viewsets.GenericViewSet,
        request: Request
    ) -> Response:

        try:
            email = request.data['email']
        except KeyError:
            raise serializers.ValidationError({
                'email': ['"email" is required']
            })

        try:
            token = request.data['token']
        except KeyError:
            raise serializers.ValidationError({
                'token': ['"token" is required']
            })

        try:
            password = request.data['password']
        except KeyError:
            raise serializers.ValidationError({
                'password': ['"password" is required']
            })

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
        self: viewsets.GenericViewSet,
        request: Request
    ) -> Response:

        try:
            email = request.data['email']
        except KeyError:
            raise serializers.ValidationError({
                'email': ['"email" is required']
            })

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

    def send_link(
        self: viewsets.GenericViewSet,
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

    def get_full_request_hostname(self):
        hostname = 'http'
        if self.request.is_secure is True:
            hostname += 's'
        hostname += '://'
        hostname += self.request.get_host()
        return hostname

    def get_user_for_token(
        self: viewsets.GenericViewSet,
        token: str,
    ) -> User:

        access_token = AccessToken.objects.get(token=token)

        return access_token.user

    def get_user_for_email_and_password(
        self: viewsets.GenericViewSet,
        email: str,
        password: str,
    ) -> User:

        user = authenticate(username=email, password=password)
        if user is None:
            raise User.DoesNotExist()

        return user

    def get_credentials_for_user_id(
        self: viewsets.GenericViewSet,
        user_id: int
    ) -> List[str]:

        application = Application.objects.get(
            user_id=user_id,
            authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS
        )

        return [
            application.client_id,
            application.raw_client_secret
        ]
