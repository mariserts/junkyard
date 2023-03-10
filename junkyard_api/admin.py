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


class ItemRelationAdmin(admin.TabularInline):
    extra = 0
    fk_name = 'child'
    raw_id_fields = ['parent', 'child']
    model = models.ItemRelation


class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemRelationAdmin, ]
    raw_id_fields = ['project', 'tenant', 'item_type']


class ProjectAdmin(admin.ModelAdmin):
    pass


class ProjectTenantAdmin(admin.ModelAdmin):
    raw_id_fields = ['project', 'tenant']


class ProjectUserAdmin(admin.ModelAdmin):
    raw_id_fields = ['project', 'user']


class TenantAdmin(admin.ModelAdmin):
    raw_id_fields = ['parent']


class ProjectTenantUserAdmin(admin.ModelAdmin):
    raw_id_fields = ['project', 'tenant', 'user']


admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.ItemType)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.ProjectTenant, ProjectTenantAdmin)
admin.site.register(models.ProjectUser, ProjectUserAdmin)
admin.site.register(models.Tenant, TenantAdmin)
admin.site.register(models.ProjectTenantUser, ProjectTenantUserAdmin)
admin.site.register(models.User, UserAdmin)
