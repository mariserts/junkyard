# -*- coding: utf-8 -*-
from django.core.signing import BadSignature, SignatureExpired
from django.db.models.query import QuerySet

from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from ..signers.exceptions import (
    BadMaxAgeException,
    BadSignatureFormatException
)
from ..signers.sign import sign_object
from ..signers.unsign import unsign_object
from ..serializers.signers import SigningSerializer, UnSigningSerializer

from .base import BaseViewSet


class SigningViewSet(
    BaseViewSet
):

    queryset = QuerySet()

    def get_serializer(
        self: BaseViewSet
    ) -> serializers.Serializer:
        if self.request.path.endswith('/sign/'):
            return SigningSerializer
        return UnSigningSerializer

    @action(
        detail=False,
        methods=['post'],
        name='Sign data',
        url_path='sign',
    )
    def sign(
        self: BaseViewSet,
        request: Request,
    ) -> Response:

        max_age = request.data.get('max_age', 0)
        salt = request.data.get('salt', '')

        try:
            data = request.data['data']
        except KeyError:
            raise serializers.ValidationError({
                'data': ['"data" is required']
            })

        if max_age is None:
            max_age = 0

        try:
            data = sign_object(data, salt=salt, max_age=max_age)
        except BadMaxAgeException:
            raise serializers.ValidationError({
                'max_age': ['"max_age" must be of type int or None']
            })

        return Response({'signature': data['signature']}, status=201)

    @action(
        detail=False,
        methods=['post'],
        name='Unsign data',
        url_path='unsign',
    )
    def unsign(
        self: BaseViewSet,
        request: Request,
    ) -> Response:

        salt = request.data.get('salt', '')

        try:
            signature = request.data['signature']
        except KeyError:
            raise serializers.ValidationError({
                'signature': ['"signature" is required']
            })

        try:
            data = unsign_object(signature, salt=salt)

        except BadSignatureFormatException as e:
            raise serializers.ValidationError({
                'signature': [e.msg(), ]
            })

        except BadMaxAgeException:
            raise serializers.ValidationError({
                'max_age': ['"max_age" must be of type int or None']
            })

        except SignatureExpired:
            return Response({'message': 'Signature expired'}, status=400)

        except BadSignature:
            return Response({'message': 'Bad signature'}, status=400)

        return Response({'data': data['data']}, status=201)
