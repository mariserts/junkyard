# -*- coding: utf-8 -*-
from typing import Type
from django.http.request import HttpRequest
from django.shortcuts import HttpResponse, render

from ..clients.items import ItemsClient

from ..components.headings import HeadingH1Component
from ..components.lists import ItemsListComponent

from .base import AuthenticatedViewSet


class CmsProjectHomePageViewSet(
    AuthenticatedViewSet
):

    template = 'junkyard_app/pages/page.html'

    def get_context(
        self: Type
    ):

        context = super().get_context()
        access_token = self.get_api_token()

        page = 1
        count = 10

        items = ItemsClient().get_items(
            access_token,
            self.kwargs['project_pk'],
            page,
            count
        )

        context['page'] = {
            'title': 'Project Overview',
            'subtitle': None
        }

        context['components'] = [
            HeadingH1Component(
                self.request,
                text=context['page']['title'],
                subtitle=context['page']['subtitle']
            ),
            ItemsListComponent(
                self.request,
                items=items['results'],
            )
        ]

        return context

    def get(
        self: Type,
        request: HttpRequest,
        project_pk: int,
    ) -> HttpResponse:

        return render(
            request,
            self.template,
            context=self.get_context()
        )
