# -*- coding: utf-8 -*-
from typing import Final

from rest_framework import permissions, viewsets

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from django_filters import rest_framework as filters

from ..pagination import JunkyardApiPagination


class BaseViewSet(viewsets.GenericViewSet):

    filter_backends: Final = (filters.DjangoFilterBackend, )
    filterset_class: Final = None
    ordering_fields = None
    pagination_class: Final = JunkyardApiPagination
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset: Final = None
    serializer_class: Final = None
