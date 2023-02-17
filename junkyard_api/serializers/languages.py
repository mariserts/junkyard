# -*- coding: utf-8 -*-
from rest_framework import serializers

from .base import BaseSerializer


class LanguageSerializer(BaseSerializer):

    code = serializers.CharField()
    name = serializers.CharField()
