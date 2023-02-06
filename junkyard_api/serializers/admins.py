# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import TenantAdmin, User


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantAdmin
        fields = '__all__'

    #
    # Field validation
    #

    def validate_tenant(self, value):

        # Tenant can not be changed if item is updated

        if self.instance is not None:
            return self.instance.tenant

        # Check tenant when creating item

        if self.request_user is None:
            raise serializers.ValidationError('No request user found')

        tenant_ids = User.get_tenants(self.request_user, format='ids')

        if value.id not in tenant_ids:
            raise serializers.ValidationError(
                f'User has no access to tenant "{value}"'
            )

        return value
