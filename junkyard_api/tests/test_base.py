# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, timezone
from typing import Type

from django.test import TestCase

from rest_framework.test import APIClient

from oauth2_provider.models import AccessToken

from ..models import Application, Tenant, Project, User


class BaseTestCase(
    TestCase
):

    def setUp(self):

        self.client = APIClient()

        self.application = Application.objects.create(
            authorization_grant_type=Application.GRANT_PASSWORD,
            client_type=Application.CLIENT_CONFIDENTIAL,
        )

        #
        self.user_one = User.objects.create(
            email='user_one@test.case'
        )
        self.user_two = User.objects.create(
            email='user_two@test.case'
        )
        self.user_three = User.objects.create(
            email='user_three@test.case'
        )

        expires = datetime.now(timezone.utc)
        expires += timedelta(hours=1)

        self.access_token_one = AccessToken.objects.create(
            application=self.application,
            expires=expires,
            scope='read write introspect',
            token='one',
            user=self.user_one,
        )
        self.access_token_two = AccessToken.objects.create(
            application=self.application,
            expires=expires,
            scope='read write introspect',
            token='two',
            user=self.user_two,
        )
        self.access_token_three = AccessToken.objects.create(
            application=self.application,
            expires=expires,
            scope='read write introspect',
            token='three',
            user=self.user_three,
        )

        #
        self.tenant_one = Tenant.objects.create(
            parent=None,
            translatable_content={'language': 'en', 'title': 'one'},
        )
        self.tenant_two = Tenant.objects.create(
            parent=self.tenant_one,
            translatable_content={'language': 'en', 'title': 'two'},
        )
        self.tenant_three = Tenant.objects.create(
            parent=self.tenant_two,
            translatable_content={'language': 'en', 'title': 'three'},
        )
        self.tenant_four = Tenant.objects.create(
            parent=self.tenant_three,
            translatable_content={'language': 'en', 'title': 'four'},
        )
        self.tenant_five = Tenant.objects.create(
            parent=self.tenant_one,
            translatable_content={'language': 'en', 'title': 'five'},
        )

        #
        self.project_one = Project.objects.create(
            name='one',
            is_active=True,
        )
        self.project_one = Project.objects.create(
            name='two'
        )
        self.project_one = Project.objects.create(
            name='three'
        )

    def authenticate_with_token(
        self: Type[TestCase],
        token: Type[AccessToken],
    ) -> None:

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token.token}'
        )
