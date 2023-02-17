# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, timezone
from typing import Type

from rest_framework.test import APITestCase

from oauth2_provider.models import AccessToken

from junkyard_api_flat_page.registry_entry import FlatPageRegistryEntry
from junkyard_api_news.registry_entry import NewsRegistryEntry

from ..models import Application, ItemType, Tenant, Project, User


class BaseTestCase(
    APITestCase
):

    def setUp(
        self: Type
    ):

        self.application = Application.objects.create(
            authorization_grant_type=Application.GRANT_PASSWORD,
            client_type=Application.CLIENT_CONFIDENTIAL,
        )

        self.item_type_flat_page = ItemType.objects.get(
            code=FlatPageRegistryEntry.code)
        self.item_type_news = ItemType.objects.get(code=NewsRegistryEntry.code)

        #
        self.user_one_email = 'user_one@test.case'
        self.user_one_password = 'user_one@pa55w0rd'

        self.user_one = User.objects.create(
            email=self.user_one_email
        )
        self.user_two = User.objects.create(
            email='user_two@test.case'
        )
        self.user_three = User.objects.create(
            email='user_three@test.case'
        )

        self.user_one.set_password(self.user_one_password)
        self.user_one.save()

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
            name='one',
        )
        self.tenant_two = Tenant.objects.create(
            parent=self.tenant_one,
            name='two',
        )
        self.tenant_three = Tenant.objects.create(
            parent=self.tenant_two,
            name='three',
        )
        self.tenant_four = Tenant.objects.create(
            parent=self.tenant_three,
            name='four',
        )
        self.tenant_five = Tenant.objects.create(
            parent=self.tenant_one,
            name='five',
        )

        #
        self.project_one = Project.objects.create(
            name='one',
            is_active=True,
        )
        self.project_two = Project.objects.create(
            name='two'
        )
        self.project_three = Project.objects.create(
            name='three'
        )

        self.project_one.item_types_for_tenants.add(self.item_type_news)
        self.project_one.item_types_for_project.add(self.item_type_flat_page)
        self.project_one.item_types_for_project.add(self.item_type_news)
        self.project_one.save()

    def authenticate_with_token(
        self: Type,
        token: Type[AccessToken],
    ) -> None:

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token.token}'
        )
