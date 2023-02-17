# -*- coding: utf-8 -*-
from rest_framework import serializers

from .base import BaseSerializer, BaseProjectUserSerializer


class ProjectUserCrudSerializer(BaseSerializer):

    project = serializers.IntegerField()
    user = serializers.IntegerField()


class ProjectUserSerializer(BaseProjectUserSerializer):
    pass
