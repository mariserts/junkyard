# -*- coding: utf-8 -*-
from typing import List, Type

from ..clients.item_types import ItemTypesClient
from ..clients.tenants import TenantsClient
from ..forms.item_filter import ItemsFilterForm
from ..forms.project_filter import ProjectsFilterForm

from .base import BaseComponent


class ProjectFilterFormComponent(
    BaseComponent
):

    template = 'junkyard_app/components/forms_projects_filter_jumbo.html'
    text = None
    wrapper_classnames = ''

    def __init__(
        self: Type,
        request: Type,
    ) -> None:

        self.request = request

    def get_form(
        self: Type,
    ) -> Type:

        return ProjectsFilterForm(
            initial=getattr(self.request, self.request.method, {}),
        )

    def get_context(
        self: Type
    ) -> dict:

        context = super().get_context()

        context['action'] = self.request.path
        context['form'] = self.get_form()
        context['method'] = 'GET'

        return context


class ItemFilterFormComponent(
    BaseComponent
):

    CACHE_TIMEOUT_ITEM_TYPE_REQUEST = 30

    template = 'junkyard_app/components/forms_items_filter_jumbo.html'
    text = None
    wrapper_classnames = ''

    def __init__(
        self: Type,
        request: Type,
        access_token: str,
        project_pk: int,
        user_id: int,
    ) -> None:

        self.access_token = access_token
        self.project_pk = project_pk
        self.request = request
        self.user_id = user_id

    def get_project_item_types_choices(
        self: Type
    ) -> List[List[str]]:

        # XXXX Cache choices

        response = ItemTypesClient().get_project_item_types(
            self.access_token,
            self.project_pk,
            for_user=self.user_id,
        )

        default_choice = [['', 'All']]
        choices = []

        for object in response.get('results', []):
            choices.append([object['code'], object['code']])

        choices = default_choice + choices

        return choices

    def get_project_tenants_choices(
        self: Type
    ) -> List[List[str]]:

        # XXXX Cache choices

        response = TenantsClient().get_project_tenants(
            self.access_token,
            self.project_pk,
        )

        default_choice = [['', 'All']]
        choices = []

        for object in response.get('results', []):
            choices.append([object['id'], object['id']])

        choices = default_choice + choices

        return choices

    def get_project_status_choices(
        self: Type
    ) -> List[List[str]]:

        return [
            ['', 'Not selected'],
            ['archived', 'Archived'],
            ['published', 'Published'],
            ['unpublished', 'Unpublished'],
        ]

    def get_form(
        self: Type,
    ) -> Type:

        return ItemsFilterForm(
            initial=getattr(self.request, self.request.method, {}),
            item_type_choices=self.get_project_item_types_choices(),
            status_choices=self.get_project_status_choices(),
            tenant_choices=self.get_project_tenants_choices(),
        )

    def get_context(
        self: Type
    ) -> dict:

        context = super().get_context()

        context['action'] = self.request.path
        context['form'] = self.get_form()
        context['method'] = 'GET'

        return context
