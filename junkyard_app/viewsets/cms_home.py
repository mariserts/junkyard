# -*- coding: utf-8 -*-
from typing import Type
from django.http.request import HttpRequest
from django.shortcuts import HttpResponse, render

from ..clients.item_types import ItemTypesClient
from ..clients.items import ItemsClient
from ..clients.tenants import TenantsClient

from .base import AuthenticatedViewSet


class CmsHomeViewSet(
    AuthenticatedViewSet
):

    template = 'junkyard_app/pages/list.html'

    def get_context(
        self: Type
    ):

        access_token = self.get_api_token()

        filter_form = None

        item_types = ItemTypesClient().get_item_types(
            access_token
        )

        items = ItemsClient().get_items(
            access_token,
            page=1,
            count=10,
        )

        tenants = TenantsClient().get_tenants(
            access_token,
            user_id=1,
            page=1,
            count=1000000
        )

        return {
            'page': {
                'title': 'CMS Overview',
                'subtitle': None
            },
            'forms': {
                'filter': filter_form,
            },
            'results': {
                'item_types': item_types,
                'items': items,
                'tenants': tenants,
            },
        }

    def get(
        self: Type,
        request: HttpRequest,
    ) -> HttpResponse:
        return render(
            request,
            self.template,
            context=self.get_context()
        )
