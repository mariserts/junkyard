# -*- coding: utf-8 -*-
from rest_framework import serializers


class SigningSerializer(serializers.Serializer):

    data = serializers.JSONField()
    max_age = serializers.IntegerField(required=False, default=0)
    salt = serializers.CharField(required=False, default='')


class UnSigningSerializer(serializers.Serializer):

    signature = serializers.CharField()
    salt = serializers.CharField(required=False, default='')
