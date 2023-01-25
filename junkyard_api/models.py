from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from . import managers
from .conf import settings


class DateTimeStampedMixin:

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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


class Tenant(
    DateTimeStampedMixin,
    models.Model
):

    owner = models.ForeignKey(
        User,
        related_name='tenants',
        on_delete=models.CASCADE,
    )

    translatable_content = models.JSONField(
        default=dict
    )


class Item(
    DateTimeStampedMixin,
    models.Model
):

    tenant = models.ForeignKey(
        Tenant,
        related_name='items',
        on_delete=models.CASCADE
    )

    item_type = models.CharField(
        max_length=255,
        choices='',
    )
    metadata = models.JSONField(
        default=dict
    )
    translatable_content = models.JSONField(
        default=dict
    )

    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
