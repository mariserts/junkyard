# -*- coding: utf-8 -*-
from typing import Type

from .test_base import BaseTestCase


class ProjectsViewSetTestCase(
    BaseTestCase
):

    def get_url(
        self: Type,
    ):
        return '/api/projects/'

    def test_list_view(
        self: Type
    ):

        request = self.client.get(self.get_url(), format='json')

        self.assertEquals(
            request.status_code,
            401
        )

    def test_create_view(
        self: Type
    ):

        request = self.client.post(
            self.get_url(),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )

    def test_retrieve_view(
        self: Type
    ):

        request = self.client.get(
            self.get_url() + f'{self.project_one.id}/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            401
        )


class AuthenticatedProjectsViewSetTestCase(
    ProjectsViewSetTestCase
):

    def test_list_view(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        request = self.client.get(self.get_url(), format='json')

        self.assertEquals(
            request.status_code,
            200
        )

    def test_create_view(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        request = self.client.post(
            self.get_url(),
            format='json'
        )

        self.assertEquals(
            request.status_code,
            403
        )

    def test_retrieve_view(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        request = self.client.get(
            self.get_url() + f'{self.project_one.id}/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            200
        )

    def test_update_view(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        request = self.client.patch(
            self.get_url() + f'{self.project_one.id}/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            403
        )

        request = self.client.put(
            self.get_url() + f'{self.project_one.id}/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            403
        )

    def test_destroy_view(
        self: Type
    ):

        self.authenticate_with_token(self.access_token_one)

        request = self.client.delete(
            self.get_url() + f'{self.project_one.id}/',
            format='json'
        )

        self.assertEquals(
            request.status_code,
            403
        )
