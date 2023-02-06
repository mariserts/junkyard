# -*- coding: utf-8 -*-
from typing import Type
from django.http.request import HttpRequest
from django.shortcuts import HttpResponse, render

from .base import PublicSiteViewSet


class PublicHomePageViewSet(
    PublicSiteViewSet
):

    template = 'junkyard_app/pages/homepage.html'

    def get_context(
        self: Type
    ):
        context = super().get_context()
        context['page'] = {
            'title': 'Homepage',
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
