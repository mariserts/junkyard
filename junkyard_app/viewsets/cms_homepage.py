# -*- coding: utf-8 -*-
from typing import Type
from django.http.request import HttpRequest
from django.shortcuts import HttpResponse, render

from ..components.headings import HeadingH1Component
from ..components.lists import ProjectsListComponent
from ..components.forms import ProjectFilterFormComponent

from .base import AuthenticatedViewSet


class CmsHomePageViewSet(
    AuthenticatedViewSet
):

    count = 500
    template = 'junkyard_app/pages/page.html'

    def get_context(
        self: Type
    ):

        context = super().get_context()

        access_token = self.get_api_token()

        context['page'] = {
            'title': 'Projects Overview',
            'subtitle': None
        }

        context['components'] = [
            HeadingH1Component(
                self.request,
                text=context['page']['title'],
                subtitle=context['page']['subtitle']
            ),
            ProjectFilterFormComponent(
                self.request
            ),
            ProjectsListComponent(
                self.request,
                access_token,
                page=1,
                count=self.count,
            )
        ]

        return context

    def get(
        self: Type,
        request: HttpRequest,
    ) -> HttpResponse:
        return render(
            request,
            self.template,
            context=self.get_context()
        )
