# -*- coding: utf-8 -*-
from django.core.signing import BadSignature, SignatureExpired
from django.db.models.query import QuerySet

from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from ..signers.exceptions import BadMaxAgeException
from ..signers.sign import sign_object
from ..signers.unsign import unsign_object
from ..serializers.signers import SigningSerializer

from .base import BaseViewSet


class SigningViewSet(
    BaseViewSet
):

    queryset = QuerySet()
    serializer_class = SigningSerializer

    @action(
        detail=False,
        methods=['post'],
        name='Sign data',
        url_path='sign',
    )
    def sign(self, request):

        max_age = request.data.get('max_age', None)
        salt = request.data.get('salt', '')

        try:
            data = request.data['data']
        except KeyError:
            raise serializers.ValidationError({
                'data': ['"data" is required']
            })

        try:
            data = sign_object(data, salt=salt, max_age=max_age)
        except BadMaxAgeException:
            raise serializers.ValidationError({
                'max_age': ['"max_age" must be of type int or None']
            })

        return Response(data, status=201)

    @action(
        detail=False,
        methods=['post'],
        name='Unsign data',
        url_path='unsign',
    )
    def unsign(self, request):

        max_age = request.data.get('max_age', None)
        salt = request.data.get('salt', '')

        try:
            data = request.data['data']
        except KeyError:
            raise serializers.ValidationError({
                'data': ['"data" is required']
            })

        try:
            data = unsign_object(data, salt=salt, max_age=max_age)

        except SignatureExpired:
            return Response({'message': 'Signature expired'}, status=400)

        except BadSignature:
            return Response({'message': 'Bad signature'}, status=400)

        except BadMaxAgeException:
            raise serializers.ValidationError({
                'max_age': ['"max_age" must be of type int or None']
            })

        return Response(data)
