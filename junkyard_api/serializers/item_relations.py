# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import ItemRelation


class ItemRelationSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = ItemRelation
        fields = '__all__'


class NestedItemRelationSerializer(serializers.Serializer):

    id = serializers.IntegerField(required=False)
    parent_id = serializers.IntegerField()
    child_id = serializers.IntegerField(required=False)
    label = serializers.CharField()
    metadata = serializers.JSONField(required=False)
