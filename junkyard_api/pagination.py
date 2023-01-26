# -*- coding: utf-8 -*-
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class JunkyardApiPagination(PageNumberPagination):

    max_page_size = 100
    page_query_param = 'page'
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page': self.page.number,
            'pages': self.page.paginator.num_pages,
            'total': self.page.paginator.count,
            'results': data
        })
