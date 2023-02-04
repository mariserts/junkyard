# -*- coding: utf-8 -*-
from typing import List

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
from rest_framework.test import APIClient

from oauth2_provider.models import AccessToken

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
    @permission_classes([permissions.AllowAny, ])
    def register(
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
            password = request.data['password']
        except KeyError:
            raise serializers.ValidationError({
                'password': ['"password" is required']
            })

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

        user = User.objects.create(email=email)
        user.set_password(password)
        user.save()

        credentials = self.get_credentials_for_user_id(user.id)

        request = APIClient().post(
            'http://0.0.0.0:8000/o/token/',
            data={
                'grant_type': Application.AUTH_GRANT_CLIENT_CREDENTIALS,
                'client_id': credentials[0],
                'client_secret': credentials[1],
            },
        )

        return Response(request.json())

    @action(
        detail=False,
        methods=['POST'],
        name='Register',
        url_path=PATH_REGISTER,
    )
    @permission_classes([permissions.IsAuthenticated, ])
    def profile(self, request):
        return Response()

    @action(
        detail=False,
        methods=['POST'],
        name='Sign in',
        url_path=PATH_SIGN_IN,
    )
    @permission_classes([permissions.AllowAny, ])
    def sign_in(
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
            password = request.data['password']
        except KeyError:
            raise serializers.ValidationError({
                'password': ['"password" is required']
            })

        try:
            user = self.get_user_for_username_and_password(email, password)
        except User.DoesNotExist as e:
            return Response(
                e.msg,
                status=404
            )

        credentials = self.get_credentials_for_user_id(user.id)

        request = APIClient().post(
            'http://0.0.0.0:8000/o/token/',
            data={
                'grant_type': Application.AUTH_GRANT_CLIENT_CREDENTIALS,
                'client_id': credentials[0],
                'client_secret': credentials[1],
            },
        )

        return Response(request.json())

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

        request = APIClient().post(
            'http://0.0.0.0:8000/o/revoke_token/',
            data={
                'token': token,
                'client_id': credentials[0],
                'client_secret': credentials[1],
            },
        )

        if request.status_code in [200, 201, 202]:
            return Response(
                {'message': 'token revoked'},
                request.status_code
            )

        return Response(
            request.json(),
            request.status_code
        )

    @action(
        detail=False,
        methods=['POST'],
        name='Change password',
        url_path=PATH_SET_PASSWORD,
    )
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

        url = 'http'
        if request.is_secure is True:
            url += 's'
        url += '://'
        url += request.get_host()
        url += reverse(
            f'authenticate-{self.PATH_SET_PASSWORD_TOKEN}',
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

    def get_user_for_token(
        self: viewsets.GenericViewSet,
        token: str,
    ) -> User:

        access_token = AccessToken.objects.get(token=token)

        return access_token.user

    def get_user_for_username_and_password(
        self: viewsets.GenericViewSet,
        email: str,
        password: str,
    ) -> User:

        user = authenticate(username=email, password=password)
        if user is not None:
            raise User.DoesNotExist(
                f'User with email "{email}" does not exist'
            )

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
