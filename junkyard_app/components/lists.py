# -*- coding: utf-8 -*-
from typing import List, Type

from django.shortcuts import reverse

from ..conf import settings
from ..clients.items import ItemsClient
from ..clients.projects import ProjectsClient

from .base import BaseComponent


class ListComponent(
    BaseComponent
):

    template = 'junkyard_app/components/list.html'
    item = []

    def __init__(
        self: Type,
        request: Type,
        items: List = [],
    ) -> None:

        self.request = request
        self.items = items

    def get_item_name(self, item):
        return ''

    def get_context(
        self: Type
    ) -> dict:

        context = super().get_context()

        items = []

        for item in self.items:
            items.append({
                'text': self.get_item_name(item),
            })

        context['items'] = items

        return context


class ListOfLinksComponent(
    ListComponent
):

    template = 'junkyard_app/components/list_of_links.html'

    def get_item_link(
        self: Type,
        item: dict,
    ) -> str:
        return '#'

    def get_item_help_text(
        self: Type,
        item: dict,
    ) -> str:
        return None

    def get_context(
        self: Type
    ) -> dict:

        context = super().get_context()

        items = []

        for item in self.items:

            items.append({
                'text': self.get_item_name(item),
                'url': self.get_item_link(item),
                'help_text': self.get_item_help_text(item),
            })

        context['items'] = items

        return context


class ItemsListComponent(
    ListOfLinksComponent
):

    access_token = None
    errors = []
    items = []
    page = 1
    pages = 1
    total = 0
    count = 10
    link_next = None
    link_previous = None

    def __init__(
        self: Type,
        request: Type,
        access_token: str,
        project_pk: int,
        page: int = 1,
        count: int = 10,
    ) -> None:

        self.access_token = access_token
        self.project_pk = project_pk
        self.request = request
        self.page = page
        self.count = count

    def set_items_data(
        self: Type
    ) -> None:

        response = ItemsClient().get_items(
            self.access_token,
            self.project_pk,
            count=self.count,
            page=self.page,
            action='update',
        )

        self.items = response['results']
        self.page = response['page']
        self.pages = response['pages']
        self.total = response['total']
        self.link_next = response['next']
        self.link_previous = response['previous']

    def get_item_name(
        self: Type,
        item: dict,
    ) -> str:

        return item['id']

    def get_item_help_text(
        self: Type,
        item: dict,
    ) -> str:

        published_text = 'Unpublished'
        if item['published'] is True:
            published_text = 'Published'

        text = f'{published_text}; '
        text += f'Item type: {item["item_type"]}; '
        text += f'Tenant: {item["tenant"]};'

        return text

    def get_item_link(
        self: Type,
        item: dict,
    ) -> str:

        return reverse(
            settings.URLNAME_CMS_PROJECT_ITEM,
            kwargs={
                'project_pk': item['project'],
                'item_pk': item['id'],
            }
        )

    def get_context(
        self: Type
    ) -> dict:

        self.set_items_data()

        context = super().get_context()

        context['pagination'] = {
            'page': self.page,
            'pages': self.pages,
            'total': self.total,
            'link_next': None,
            'link_previous': None,
        }

        return context


class ProjectsListComponent(
    ListOfLinksComponent
):

    errors = []
    items = []
    page = 1
    pages = 1
    total = 0
    count = 10
    link_next = None
    link_previous = None

    def __init__(
        self: Type,
        request: Type,
        access_token: str,
        page: int = 1,
        count: int = 10,
    ) -> None:

        self.access_token = access_token
        self.request = request
        self.page = page
        self.count = count

    def set_items_data(
        self: Type
    ) -> None:

        response = ProjectsClient().get_projects(
            self.access_token,
            action='create_items',
            count=self.count,
            page=self.page,
        )

        self.items = response['results']
        self.page = response['page']
        self.pages = response['pages']
        self.total = response['total']
        self.link_next = response['next']
        self.link_previous = response['previous']

    def get_item_name(
        self: Type,
        item: dict,
    ) -> str:

        return item['name']

    def get_item_link(
        self: Type,
        item: dict,
    ) -> str:

        return reverse(
            settings.URLNAME_CMS_PROJECT_HOMEPAGE,
            kwargs={'project_pk': item['id']}
        )

    def get_context(
        self: Type
    ) -> dict:

        self.set_items_data()

        context = super().get_context()

        context['pagination'] = {
            'page': self.page,
            'pages': self.pages,
            'total': self.total,
            'link_next': None,
            'link_previous': None,
        }

        return context
