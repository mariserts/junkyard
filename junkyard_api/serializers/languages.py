# -*- coding: utf-8 -*-
from rest_framework import serializers


class LanguageSerializer(serializers.Serializer):

    code = serializers.CharField()
    name = serializers.CharField()
