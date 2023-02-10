# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import ProjectTenantUser


class ProjectTenantUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectTenantUser
        fields = '__all__'
