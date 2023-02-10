# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import ProjectUser


class ProjectUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectUser
        fields = '__all__'
