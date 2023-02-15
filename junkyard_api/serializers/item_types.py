# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import ItemType


class ItemTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemType
        fields = '__all__'
