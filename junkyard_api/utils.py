# -*- coding: utf-8 -*-
from .serializers.tenants import TenantSerializer
from .serializers.users import UserSerializer


def get_tenant_serializer():
    return TenantSerializer


def get_user_serializer():
    return UserSerializer
