# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import ItemRelation


class ItemRelationSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = ItemRelation
        fields = '__all__'
