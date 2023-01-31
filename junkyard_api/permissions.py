# -*- coding: utf-8 -*-
from rest_framework import permissions

from .models import Tenant


class ReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return False


class TenantUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        id = view.kwargs.get('pk', '-1')
        tenant_id = view.kwargs.get('tenant_pk', id)

        if tenant_id == '-1':
            return True

        return Tenant.user_has_access(tenant_id, request.user.id)
