# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .django.admin.custom_user_forms import (
    CustomUserChangeForm,
    CustomUserCreationForm
)
from . import models


class UserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = models.User

    list_display = (
        'id',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'email',
        'is_staff',
        'is_active',
    )

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'password'
                )
            }
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_staff',
                    'is_active',
                    'is_superuser',
                )
            }
        ),
    )

    add_fieldsets = (
        (
            None, {
                'classes': (
                    'wide',
                ),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_active',
                    'is_superuser',
                )
            }
        ),
    )

    search_fields = (
        'email',
    )

    ordering = (
        'email',
    )


admin.site.register(models.Item)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tenant)
admin.site.register(models.TenantAdmin)
