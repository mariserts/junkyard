# -*- coding: utf-8 -*-
from typing import Type
from django.http.request import HttpRequest
from django.shortcuts import HttpResponse, render

from .base import AuthenticatedViewSet


class CmsProjectItemViewSet(
    AuthenticatedViewSet
):

    template = 'junkyard_app/pages/page.html'

    def get_context(
        self: Type
    ):
        context = super().get_context()
        context['page'] = {
            'title': 'Item detail',
            'subtitle': None
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
