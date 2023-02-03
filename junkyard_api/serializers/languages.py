# -*- coding: utf-8 -*-
from rest_framework import serializers


class LanguageSerializer(serializers.Serializer):

    code = serializers.CharField()
    default = serializers.BooleanField(default=False, required=False)
    name = serializers.CharField()
