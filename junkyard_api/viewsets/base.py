# -*- coding: utf-8 -*-
from rest_framework import permissions, viewsets

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from django_filters import rest_framework as filters

from ..pagination import JunkyardApiPagination


class BaseViewSet(viewsets.GenericViewSet):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = None
    ordering_fields = None
    pagination_class = JunkyardApiPagination
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = None
    serializer_class = None
