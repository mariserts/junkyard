# -*- coding: utf-8 -*-
from typing import Type

from django.test import TestCase

from ..models import (
    Project,
    ProjectTenant,
    ProjectTenantUser,
    ProjectUser,
    Tenant,
    User
)


class UserModelTestCase(
    TestCase
):

    def setUp(
        self: Type
    ) -> None:

        self.project_one = Project.objects.create(name='one')
        self.project_two = Project.objects.create(name='two')

        self.user_one = User.objects.create(email='user_one@text.case')
        self.user_two = User.objects.create(email='user_two@text.case')

        self.tenant_one = Tenant.objects.create(
            name='one',
            is_active=True
        )

        self.tenant_two = Tenant.objects.create(
            name='two',
            parent=self.tenant_one,
            is_active=True
        )

        self.tenant_three = Tenant.objects.create(
            name='three',
            parent=self.tenant_two,
            is_active=True
        )

        self.tenant_four = Tenant.objects.create(
            name='four',
            parent=self.tenant_three,
            is_active=True
        )

        self.tenant_five = Tenant.objects.create(
            name='five',
            parent=self.tenant_one,
            is_active=True
        )

    def tearDown(
        self: Type
    ) -> None:

        Project.objects.all().delete()
        Tenant.objects.all().delete()
        User.objects.all().delete()

    def test_user_permission_set_one(self):

        with self.assertNumQueries(3):
            pset = self.user_one.permission_set.dict()

        self.assertEquals(
            len(pset['projects'].keys()),
            0
        )

    def test_user_permission_set_two(self):

        ProjectTenant.objects.create(
            tenant=self.tenant_one,
            project=self.project_one,
        )

        ProjectUser.objects.create(
            user=self.user_one,
            project=self.project_one,
        )

        with self.assertNumQueries(4):
            pset = self.user_one.permission_set.dict()

        self.assertEquals(
            len(pset['projects'].keys()),
            1
        )

    def test_user_permission_set_three(self):

        ProjectTenantUser.objects.create(
            user=self.user_one,
            tenant=self.tenant_two,
            project=self.project_two,
        )

        with self.assertNumQueries(3):
            pset = self.user_one.permission_set.dict()

        self.assertEquals(
            len(pset['projects'].keys()),
            0
        )

    def test_user_permission_set_four(self):

        ProjectTenant.objects.create(
            tenant=self.tenant_two,
            project=self.project_two,
        )

        ProjectTenantUser.objects.create(
            user=self.user_one,
            tenant=self.tenant_two,
            project=self.project_two,
        )

        with self.assertNumQueries(5):
            pset = self.user_one.permission_set.dict()

        self.assertEquals(
            len(pset['projects'].keys()),
            1
        )

        self.assertIs(
            str(self.project_two.id) in pset['projects'].keys(),
            True
        )

        self.assertIs(
            str(self.project_one.id) in pset['projects'].keys(),
            False
        )

    def test_user_permission_set_five(self):

        # Confirm N+1 query problem if project count increases

        ProjectTenant.objects.create(
            tenant=self.tenant_one,
            project=self.project_one,
        )

        ProjectTenant.objects.create(
            tenant=self.tenant_two,
            project=self.project_two,
        )

        ProjectTenantUser.objects.create(
            user=self.user_one,
            tenant=self.tenant_one,
            project=self.project_one,
        )

        ProjectTenantUser.objects.create(
            user=self.user_one,
            tenant=self.tenant_two,
            project=self.project_two,
        )

        with self.assertNumQueries(7):
            pset = self.user_one.permission_set.dict()

        self.assertEquals(
            len(pset['projects'].keys()),
            2
        )

    def test_user_permission_set_six(self):

        ProjectUser.objects.create(
            user=self.user_one,
            project=self.project_two,
        )

        with self.assertNumQueries(4):
            pset = self.user_one.permission_set.dict()

        self.assertEquals(
            len(pset['projects'].keys()),
            1
        )

        self.assertIs(
            str(self.project_two.id) in pset['projects'].keys(),
            True
        )
