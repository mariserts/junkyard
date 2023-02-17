# -*- coding: utf-8 -*-
from rest_framework import serializers

from .base import BaseItemRelationSerializer, BaseSerializer


class ItemRelationSerializer(BaseItemRelationSerializer):
    pass


class CrudItemRelationSerializer(BaseSerializer):

    id = serializers.IntegerField(allow_null=True, required=False)
    parent = serializers.IntegerField()
    child = serializers.IntegerField(allow_null=True, required=False)
    label = serializers.CharField()

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
