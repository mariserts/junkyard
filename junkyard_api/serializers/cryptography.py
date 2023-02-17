# -*- coding: utf-8 -*-
from rest_framework import serializers

from .base import BaseSerializer


class SigningSerializer(BaseSerializer):

    data = serializers.JSONField()
    max_age = serializers.IntegerField(required=False, default=0)
    salt = serializers.CharField(required=False, default='')


class UnSigningSerializer(BaseSerializer):

    signature = serializers.CharField()
    salt = serializers.CharField(required=False, default='')
