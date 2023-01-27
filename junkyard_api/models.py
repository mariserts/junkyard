# -*- coding: utf-8 -*-
from typing import List

from django.core.cache import cache
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet

from . import managers
from .conf import settings


class User(AbstractUser):

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.CustomUserManager()

    def save(self, *args, **kwargs):

        if self.email in [None, '', ' ']:
            raise ValidationError('Email is required')

        self.email = self.email.lower()
        self.username = self.email

        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class Tenant(models.Model):

    CACHE_TIMEOUT_GET_ALL_CHILDREN_IDS = 10
    CACHE_TIMEOUT_GET_ALL_PARENTS_IDS = 10
    CACHE_TIMEOUT_USER_HAS_ACCESS = 10

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tenants',
    )
    parent = models.ForeignKey(
        'Tenant',
        on_delete=models.CASCADE,
        related_name='children',
        blank=True,
        null=True
    )

    translatable_content = models.JSONField(
        default=dict
    )

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        default = f'ID: {self.id}'
        translatable_content = self.translatable_content

        if len(translatable_content) > 0:
            return translatable_content[0].get('title', default)

        return default

    @staticmethod
    def get_all_children(
        instance: models.Model
    ) -> QuerySet:

        """

        Get all children for instance

        Attrs:
        - instance: Tenant - instance of tenant

        Returns:
        - QuerySet - list of children

        """

        # Query count will increase with children count, n+1 problem

        children = instance.children.all().only('id')

        for child in children:
            children = children.union(Tenant.get_all_children(child))

        return children

    @staticmethod
    def get_all_children_ids(
        instance: models.Model
    ) -> List[int]:

        """

        Get all children ids for instance

        Cached for CACHE_TIMEOUT_GET_ALL_CHILDREN_IDS of time

        Attrs:
        - instance: Tenant - instance of tenant

        Returns:
        - List[int] - list of children ids

        """

        cache_key = f'models.Tenant.get_all_children_ids__{instance.id}'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        queryset = Tenant.get_all_children(
            instance
        ).values_list(
            'id',
            flat=True
        )

        ids = list(set(list(queryset)))

        cache.set(
            cache_key,
            ids,
            Tenant.CACHE_TIMEOUT_GET_ALL_CHILDREN_IDS
        )

        return ids

    @staticmethod
    def get_all_parents(
        instance: models.Model
    ) -> QuerySet:

        """

        Get all parents for instance

        Attrs:
        - instance: Tenant - instance of tenant

        Returns:
        - QuerySet - list of parents

        """

        parent = instance.parent
        if parent is None:
            return Tenant.objects.none()

        queryset = Tenant.objects.filter(id=instance.parent_id)

        parents = queryset.union(Tenant.get_all_parents(instance.parent))

        return parents

    @staticmethod
    def get_all_parents_ids(
        instance: models.Model
    ) -> List[int]:

        """

        Get all parents ids for instance

        Cached for CACHE_TIMEOUT_GET_ALL_PARENTS_IDS of time

        Attrs:
        - instance: Tenant - instance of tenant

        Returns:
        - List[int] - list of parent ids

        """

        cache_key = f'models.Tenant.get_all_parents_ids__{instance.id}'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        queryset = Tenant.get_all_parents(
            instance
        ).values_list(
            'id',
            flat=True
        )

        ids = list(set(list(queryset)))

        cache.set(
            cache_key,
            ids,
            Tenant.CACHE_TIMEOUT_GET_ALL_PARENTS_IDS
        )

        return ids

    @staticmethod
    def user_has_access(
        tenant_id: int,
        user_id: int,
    ) -> bool:

        """

        Get permission for user for tenant, if permission is cascading
        then allow nested tenant permission

        Cached for CACHE_TIMEOUT_USER_HAS_ACCESS of time

        Attrs:
        - tenant_id int: tenant id
        - user_id int: user id

        Returns
        - bool

        """

        cascade = settings.CASCADE_TENANT_PERMISSIONS

        cache_key = f'models.Tenant.user_has_access__{tenant_id}__{user_id}'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        # Check if user is admin of current tenant

        queryset = Tenant.objects.filter(
            id=tenant_id
        )

        condition = Q()
        condition.add(Q(owner_id=user_id), Q.OR)
        condition.add(Q(admins__user_id=user_id), Q.OR)

        queryset = queryset.filter(
            condition
        ).prefetch_related(
            'admins'
        ).exists()

        if queryset is True:
            cache.set(
                cache_key,
                queryset,
                Tenant.CACHE_TIMEOUT_USER_HAS_ACCESS
            )
            return queryset

        # if not and cascade is False return False

        if queryset is False and cascade is False:
            cache.set(
                cache_key,
                queryset,
                Tenant.CACHE_TIMEOUT_USER_HAS_ACCESS
            )
            return queryset


        tenant = Tenant.objects.filter(id=tenant_id).first()
        if tenant is None:
            cache.set(
                cache_key,
                False,
                Tenant.CACHE_TIMEOUT_USER_HAS_ACCESS
            )
            return False

        # if cascade is true check if user is admin of one of parent tenants

        parent_ids = Tenant.get_all_parents_ids(tenant)

        queryset = Tenant.objects.filter(
            id__in=parent_ids
        )

        condition = Q()
        condition.add(Q(owner_id=user_id), Q.OR)
        condition.add(Q(admins__user_id=user_id), Q.OR)

        queryset = queryset.filter(
            condition
        ).prefetch_related(
            'admins'
        ).exists()

        cache.set(
            cache_key,
            queryset,
            Tenant.CACHE_TIMEOUT_USER_HAS_ACCESS
        )

        return queryset

class TenantAdmin(models.Model):

    class Meta:
        unique_together = (
            'tenant',
            'user'
        )

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='admins',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tenants_to_admin',
    )
    acl = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'User: {self.user} Tenant: {self.tenant}'


class Item(models.Model):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='items',
    )

    item_type = models.CharField(
        db_index=True,
        max_length=255,
    )
    metadata = models.JSONField(
        blank=True,
        default=dict,
        null=True
    )
    translatable_content = models.JSONField(
        blank=True,
        default=dict,
        null=True
    )

    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        default = f'ID: {self.id} | {self.item_type}'
        translatable_content = self.translatable_content

        if len(translatable_content) > 0:
            return translatable_content[0].get('title', default)

        return default
