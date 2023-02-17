# -*- coding: utf-8 -*-
from rest_framework import serializers

from .. import models


class BaseSerializer(serializers.Serializer):
    pass


class BaseModelSerializer(serializers.ModelSerializer):
    pass


class BaseItemSerializer(BaseModelSerializer):

    class Meta:
        model = models.Item
        fields = '__all__'


class BaseItemRelationSerializer(BaseModelSerializer):

    class Meta:
        model = models.ItemRelation
        fields = '__all__'


class BaseItemTypeSerializer(BaseModelSerializer):

    class Meta:
        model = models.ItemType
        fields = '__all__'


class BaseProjectSerializer(BaseModelSerializer):

    class Meta:
        model = models.Project
        fields = '__all__'


class BaseProjectTenantSerializer(BaseModelSerializer):

    class Meta:
        model = models.ProjectTenant
        fields = '__all__'


class BaseProjectTenantUserSerializer(BaseModelSerializer):

    class Meta:
        model = models.ProjectTenantUser
        fields = '__all__'


class BaseProjectUserSerializer(BaseModelSerializer):

    class Meta:
        model = models.ProjectUser
        fields = '__all__'


class BaseTenantSerializer(BaseModelSerializer):

    class Meta:
        model = models.Tenant
        fields = '__all__'


class BaseUserSerializer(BaseModelSerializer):

    class Meta:
        model = models.User
        exclude = [
            'groups',
            'is_staff',
            'is_superuser',
            'password',
            'user_permissions',
            'username',
        ]
