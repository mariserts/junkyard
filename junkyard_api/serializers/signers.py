# -*- coding: utf-8 -*-
from rest_framework import serializers


class SigningSerializer(serializers.Serializer):

    data = serializers.JSONField()
    max_age = serializers.IntegerField(required=False)
    salt = serializers.CharField(required=False)
