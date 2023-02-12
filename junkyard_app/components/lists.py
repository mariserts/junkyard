# -*- coding: utf-8 -*-
from typing import List, Type

from django.shortcuts import reverse

from ..conf import settings

from .base import BaseComponent


class ListComponent(
    BaseComponent
):

    request = None
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


class ProjectsListComponent(
    ListOfLinksComponent
):

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
