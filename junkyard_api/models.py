# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from . import managers


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
