# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import SearchVector


class SearchVectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchVector
        fields = '__all__'
