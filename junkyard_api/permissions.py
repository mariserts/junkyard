# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.db.models import Q

from rest_framework import permissions

from .models import Tenant


class AuthenticatedUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated is True


class TenantUserPermission(permissions.BasePermission):

    _user_has_permission = None

    def has_permission(self, request, view):

        id = view.kwargs.get('pk', None)
        tenant_pk = view.kwargs.get('tenant_pk', id)
        user_id = request.user.id

        cache_key = f'permissions.TenantUserPermission__{tenant_pk}__{user_id}'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        queryset = Tenant.objects.filter(
            id=tenant_pk
        )

        condition = Q()
        condition.add(Q(owner_id=user_id), Q.OR)
        condition.add(Q(admins__user_id=user_id), Q.OR)

        queryset = queryset.filter(
            condition
        ).prefetch_related(
            'admins'
        ).exists()

        cache.set(cache_key, queryset, 5)

        return queryset
