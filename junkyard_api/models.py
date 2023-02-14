# -*- coding: utf-8 -*-
from typing import List, Type, Union

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet

from networkx import DiGraph
from networkx.exception import NetworkXError
from networkx.algorithms.dag import descendants

from oauth2_provider.models import AbstractApplication

from .conf import settings
from .managers import CustomUserManager


class ItemType(models.Model):

    code = models.CharField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Application(AbstractApplication):

    raw_client_secret = models.CharField(
        max_length=255,
        blank=True,
    )

    def save(
        self: Type[models.Model],
        *args: List,
        **kwargs: dict,
    ) -> None:

        creation = self.id is None
        if creation is True:
            self.raw_client_secret = self.client_secret

        super().save(*args, **kwargs)


class User(AbstractUser):

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(
        self: Type[models.Model],
        *args: List,
        **kwargs: dict,
    ) -> None:

        self.email = self.email.lower()
        self.username = self.email

        super(User, self).save(*args, **kwargs)

    @property
    def permission_set(self):
        attr_name = '_permission_set'
        if getattr(self, attr_name, None) is None:
            setattr(self, attr_name, PermissionSet(self))
        return getattr(self, attr_name)


class Project(models.Model):

    description = models.CharField(max_length=4096, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    item_types_for_tenants = models.ManyToManyField(
        ItemType,
        related_name='for_tenants',
        blank=True
    )
    item_types_for_project = models.ManyToManyField(
        ItemType,
        related_name='for_projects',
        blank=True
    )

    is_public = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProjectUser(models.Model):

    project = models.ForeignKey(
        Project,
        related_name='users',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='projects',
        on_delete=models.CASCADE
    )
    acl = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tenant(models.Model):

    parent = models.ForeignKey(
        'Tenant',
        related_name='children',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    translatable_content = models.JSONField(default=list)
    is_active = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_graph():

        # XXXX Cache list(G.nodes)
        # Can add this after Tenant.save()
        # Or in post.save() signal

        G = DiGraph()

        for tenant in Tenant.objects.all():

            parent_node = tenant.parent_id
            tenant_node = tenant.id

            if parent_node is not None:
                G.add_edge(parent_node, tenant_node)

        return G

    def get_all_children(
        self: Type,
        format: str = 'queryset'
    ) -> QuerySet:

        G = Tenant.get_graph()

        try:
            ids = list(descendants(G, self.id))
        except NetworkXError:

            if format == 'ids':
                return []

            return Tenant.objects.none()

        if format == 'ids':
            return ids

        return Tenant.objects.filter(id__in=ids)


class ProjectTenant(models.Model):

    project = models.ForeignKey(
        Project,
        related_name='tenants',
        on_delete=models.CASCADE
    )
    tenant = models.ForeignKey(
        Tenant,
        related_name='projects',
        on_delete=models.CASCADE
    )

    is_active = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProjectTenantUser(models.Model):

    class Meta:
        unique_together = (
            'project',
            'tenant',
            'user'
        )

    project = models.ForeignKey(
        Project,
        related_name='tenant_users',
        on_delete=models.CASCADE
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='users',
    )
    user = models.ForeignKey(
        User,
        related_name='tenants',
        on_delete=models.CASCADE,
    )
    acl = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Item(models.Model):

    project = models.ForeignKey(
        Project,
        related_name='items',
        on_delete=models.CASCADE,
    )
    tenant = models.ForeignKey(
        Tenant,
        related_name='items',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    moved_to = models.ForeignKey(
        'Item',
        related_name='predecessor',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    item_type = models.ForeignKey(
        ItemType,
        related_name='items',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    metadata = models.JSONField(
        blank=True,
        default=dict,
        null=True
    )
    translatable_content = models.JSONField(
        blank=True,
        default=list,
        null=True
    )

    archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(blank=True, null=True)

    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(
        self: Type,
    ) -> str:
        return f'ID: {self.id} | {self.item_type}'


class ItemRelation(models.Model):

    parent = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='child_items'
    )
    child = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='parent_items'
    )
    label = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    metadata = models.JSONField(
        blank=True,
        default=dict,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PermissionSet:

    pset = None
    user = None

    def __init__(
        self: Type,
        user: Type[User],
    ) -> None:

        self.user = user
        self.pset = self.get_permissions_set()

    #
    #
    #

    def get_projects(
        self: Type
    ) -> List[int]:
        return list(map(lambda key: int(key), self.pset['projects'].keys()))

    def get_project_tenants(
        self: Type,
        project_pk: Union[int, str],
    ) -> List[int]:

        if self.is_project_user(project_pk) is True:
            return []

        tenants = self.pset['projects'].get(
            str(project_pk),
            {}
        ).get(
            'tenants',
            None
        )

        if tenants is None:
            return [-1, ]

        return list(map(lambda key: int(key), tenants.keys()))

    #
    #
    #

    def is_project_user(
        self: Type,
        project_pk: Union[int, str],
    ) -> bool:
        return self.pset['projects'].get(
            str(project_pk),
            {}
        ).get(
            'is_user',
            False
        )

    def is_project_tenant_user(
        self: Type,
        project_pk: Union[int, str],
        tenant_pk: Union[int, str],
    ) -> bool:

        if self.is_project_user(project_pk) is True:
            return True

        return self.pset['projects'].get(
            str(project_pk),
            {}
        ).get('tenants', {}).get(
            str(tenant_pk),
            {}
        ).get(
            'is_user',
            False
        )

        return False

    #
    #
    #

    def get_permissions_set(
        self: Type
    ) -> dict:

        # XXXX Cache

        data = {
            'projects': {}
        }

        if isinstance(self.user, User) is False:
            return data

        # Get all Projects where user is ProjectUser

        pu_objects = ProjectUser.objects.filter(
            user=self.user,
            user__is_active=True,
            project__is_active=True,
        ).select_related(
            'project',
            'user',
        ).only(
            'id',
            'acl',
            'project_id',
            'user_id',
        )

        for object in pu_objects:
            data['projects'][str(object.project_id)] = {
                'acl': object.acl,
                'id': object.project_id,
                'is_user': True,
                'tenants': {},
            }

        # Get all Projects where user is TenantUser

        project_ids_to_exclude = list(
            pu_objects.values_list('project_id', flat=True)
        )

        ptu_objects = ProjectTenantUser.objects.filter(
            user=self.user,
            project__is_active=True,
            tenant__is_active=True,
            tenant__projects__is_active=True,
        ).select_related(
            'project',
            'tenant',
        ).prefetch_related(
            'tenant__projects',
        ).exclude(
            project_id__in=project_ids_to_exclude
        ).only(
            'id',
            'acl',
            'project_id',
            'tenant_id',
        )

        tenant_ids_to_exclude = []

        for object in ptu_objects:

            tenant_ids_to_exclude.append(object.tenant_id)

            project_pk = str(object.project_id)
            tenant_pk = str(object.tenant_id)

            if project_pk not in data['projects']:
                data['projects'][project_pk] = {
                    'acl': None,
                    'id': object.project_id,
                    'is_user': False,
                    'tenants': {},
                }

            data['projects'][project_pk]['tenants'][tenant_pk] = {
                'acl': object.acl,
                'id': object.tenant.id,
                'is_user': True,
            }

        # Get all nested tenants in permissions cascade

        if settings.CASCADE_TENANT_PERMISSIONS is True:

            G = Tenant.get_graph()

            projects_to_iter = list(
                map(
                    lambda project_pk:
                        int(project_pk),
                    data['projects'].keys()
                )
            )

            projects_to_iter = list(
                set(projects_to_iter).difference(set(project_ids_to_exclude))
            )

            for project_id in projects_to_iter:

                tenants = data['projects'][str(project_id)].get('tenants', {})

                ids = sum(
                    list(
                        map(
                            lambda id:
                                list(descendants(G, int(id))),
                            tenants.keys()
                        )
                    ),
                    []
                )

                nested_tenant_objects = ProjectTenant.objects.filter(
                    is_active=True,
                    project_id=project_id,
                    project__is_active=True,
                    tenant__pk__in=ids,
                    tenant__is_active=True,
                ).exclude(
                    project_id__in=project_ids_to_exclude,
                ).exclude(
                    tenant_id__in=tenant_ids_to_exclude,
                ).select_related(
                    'project',
                    'tenant',
                ).only(
                    'tenant_id',
                    'project',
                )

                for object in nested_tenant_objects:

                    tenant_pk = str(object.tenant_id)

                    data['projects'][str(project_id)]['tenants'][tenant_pk] = {
                        'acl': 'cascading-permission',
                        'id': object.tenant_id,
                        'is_user': True
                    }

        # Get all item types for project

        for project_pk in data['projects'].keys():

            if data['projects'][project_pk]['is_user'] is True:

                condition = Q()
                condition.add(Q(for_tenants__pk=project_pk), Q.OR)
                condition.add(Q(for_projects__pk=project_pk), Q.OR)

                queryset = ItemType.objects.filter(
                    condition
                ).only(
                    'code'
                )

            else:

                queryset = ItemType.objects.filter(
                    for_tenants__pk=project_pk
                ).only(
                    'code'
                )

            queryset = queryset.values_list('code', flat=True)

            data['projects'][project_pk]['item_types'] = list(queryset)

        return data

    def dict(self):
        return self.pset
