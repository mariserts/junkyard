# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import TenantAdmin


class TenantAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantAdmin
        fields = '__all__'
