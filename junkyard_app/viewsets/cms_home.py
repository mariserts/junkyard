# -*- coding: utf-8 -*-
from django.http.request import HttpRequest
from django.shortcuts import HttpResponse, render

from .base import BaseViewSet


class CmsHomeViewSet(BaseViewSet):

    template = 'junkyard_app/pages/list.html'

    def get_context(
        self: BaseViewSet
    ):

        form = None

        return {
            'page': {
                'title': 'CMS Overview',
                'subtitle': None
            },
            'forms': {
                'filter': form,
            },
            'results': {
                'total': 0,
                'page': 1,
                'pages': 1,
                'results': [],
            },
        }

    def get(
        self: BaseViewSet,
        request: HttpRequest,
    ) -> HttpResponse:
        return render(
            request,
            self.template,
            context=self.get_context()
        )
