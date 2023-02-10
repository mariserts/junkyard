# -*- coding: utf-8 -*-
from typing import Type
from django.http.request import HttpRequest
from django.shortcuts import HttpResponse, render

from ..clients.projects import ProjectsClient

from .base import AuthenticatedViewSet


class CmsHomePageViewSet(
    AuthenticatedViewSet
):

    template = 'junkyard_app/pages/list.html'

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
            'projects': projects
        }

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
