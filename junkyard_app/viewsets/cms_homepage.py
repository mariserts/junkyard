# -*- coding: utf-8 -*-
from typing import Type
from django.http.request import HttpRequest
from django.shortcuts import HttpResponse, render

from ..clients.projects import ProjectsClient
from ..components.headings import HeadingH1Component
from ..components.lists import ProjectsListComponent

from .base import AuthenticatedViewSet


class CmsHomePageViewSet(
    AuthenticatedViewSet
):

    template = 'junkyard_app/pages/page.html'

    def get_context(
        self: Type
    ):

        context = super().get_context()

        access_token = self.get_api_token()

        projects = ProjectsClient().get_projects(access_token)

        context['page'] = {
            'title': 'CMS Overview',
            'subtitle': None
        }

        context['results'] = {
            'list_items': projects['results']
        }

        context['components'] = [
            HeadingH1Component(
                self.request,
                text=context['page']['title'],
                subtitle=context['page']['subtitle']
            ),
            ProjectsListComponent(
                self.request,
                items=projects['results']
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
