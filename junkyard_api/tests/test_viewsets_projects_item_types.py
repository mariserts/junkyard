# -*- coding: utf-8 -*-
from typing import Type, Union

from ..filtersets.projects_item_types import ProjectsItemTypesFilterSet
from ..models import ProjectUser, ProjectTenant, ProjectTenantUser
from ..utils.urls import get_projects_item_types_url

from .test_base import BaseTestCase


class ProjectsItemTypesViewSetTestCase(
    BaseTestCase
):

    def get_url(
        self: Type,
        project_pk: Union[str, int]
    ):
        return get_projects_item_types_url(None, project_pk)

    def test_list_view(
        self: Type
    ):

        request = self.client.get(
            self.get_url(self.project_one.id),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )


class AuthenticatedProjectsItemTypesViewSetTestCase(
    ProjectsItemTypesViewSetTestCase
):

    def test_list_view(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        request = self.client.get(
            self.get_url(self.project_one.id),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_list_view_filter_by_used_by(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        base_url = self.get_url(self.project_one.id)

        url = base_url + '?used_by='
        url += f'{ProjectsItemTypesFilterSet.CHOICE_USED_BY_PROJECT[0]}'

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        data = request.json()

        self.assertEquals(
            data['total'],
            2
        )

        url = base_url + '?used_by='
        url += f'{ProjectsItemTypesFilterSet.CHOICE_USED_BY_TENANT[0]}'

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        data = request.json()

        self.assertEquals(
            data['total'],
            1
        )

        self.assertEquals(
            data['results'][0]['code'],
            self.item_type_news.code
        )

    def test_list_view_filter_by_for_user_not_a_project_user(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        base_url = self.get_url(self.project_one.id)

        url = base_url + f'?for_user={self.user_one.id}'

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        data = request.json()

        self.assertEquals(
            data['total'],
            0
        )

    def test_list_view_filter_by_for_user_project_user(
        self: Type
    ):

        project_user = ProjectUser.objects.create(
            project=self.project_one,
            user=self.user_one
        )

        self.authenticate_with_token(self.access_token_one)

        base_url = self.get_url(self.project_one.id)

        url = base_url + f'?for_user={self.user_one.id}'

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        data = request.json()

        self.assertEquals(
            data['total'],
            2
        )

        project_user.delete()

        ProjectTenant.objects.create(
            project=self.project_one,
            tenant=self.tenant_one
        )

        ProjectTenantUser.objects.create(
            project=self.project_one,
            tenant=self.tenant_one,
            user=self.user_one
        )

        url = base_url + f'?for_user={self.user_one.id}'

        request = self.client.get(
            url,
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

        data = request.json()

        self.assertEquals(
            data['total'],
            1
        )

        self.assertEquals(
            data['results'][0]['code'],
            self.item_type_news.code
        )
