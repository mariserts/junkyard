# -*- coding: utf-8 -*-
from typing import Type

from django.core.signing import BadSignature, SignatureExpired
from django.db.models.query import QuerySet

from rest_framework import permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from ..cryptography.exceptions import (
    BadMaxAgeException,
    BadSignatureFormatException
)
from ..cryptography.sign import sign_object
from ..cryptography.unsign import unsign_object
from ..serializers.cryptography import SigningSerializer, UnSigningSerializer


class CryptographyViewSet(
    viewsets.GenericViewSet
):

    permission_classes = (permissions.IsAuthenticated, )
    queryset = QuerySet()
    serializer_class = SigningSerializer

    def get_serializer_class(
        self: Type
    ) -> Type:

        if self.action == 'sign':
            return self.serializer_class

        return UnSigningSerializer

    @action(
        detail=False,
        methods=['post'],
        name='Sign data',
        url_path='sign',
    )
    def sign(
        self: Type,
        request: Type[Request],
    ) -> Type[Response]:

        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid() is False:
            return Response(
                serializer.errors,
                status=400
            )

        data = serializer.validated_data.get('data', {})
        max_age = serializer.validated_data.get('max_age', 0)
        salt = serializer.validated_data.get('salt', '')

        data = sign_object(data, salt=salt, max_age=max_age)

        return Response(
            {'signature': data['signature']},
            status=201
        )

    @action(
        detail=False,
        methods=['post'],
        name='Unsign data',
        url_path='unsign',
    )
    def unsign(
        self: Type,
        request: Type[Request],
    ) -> Type[Response]:

        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid() is False:
            return Response(
                serializer.errors,
                status=400
            )

        salt = serializer.validated_data.get('salt', '')
        signature = serializer.validated_data.get('signature', '')

        try:
            data = unsign_object(signature, salt=salt)

        except BadSignatureFormatException:
            raise ValidationError({
                'signature': 'Bad signature format'
            })

        except BadMaxAgeException:
            raise ValidationError({
                'max_age': ['"max_age" must be of type int or None']
            })

        except SignatureExpired:
            return Response(
                {'message': 'Signature expired'},
                status=400
            )

        except BadSignature:
            return Response(
                {'message': 'Bad signature'},
                status=400
            )

        return Response(
            {'data': data['data']},
            status=201
        )
