# -*- coding: utf-8 -*-
from rest_framework import permissions

from .models import Tenant


class AuthenticatedUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated is True


class TenantUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        id = view.kwargs.get('pk', '-1')
        tenant_id = view.kwargs.get('tenant_pk', id)

        if tenant_id is -1:
            return True

        return Tenant.user_has_access(tenant_id, request.user.id)
