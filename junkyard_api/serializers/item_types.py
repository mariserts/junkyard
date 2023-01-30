# -*- coding: utf-8 -*-
from rest_framework import serializers


class ItemTypeSerializer(serializers.Serializer):

    name = serializers.CharField()
    schema = serializers.JSONField(default={})
