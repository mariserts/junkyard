# -*- coding: utf-8 -*-
from typing import List, Type

from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from ..conf import settings
from ..filtersets.languages import LanguagesFilterSet
from ..serializers.languages import LanguageSerializer


class LanguagesViewSet(
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = LanguagesFilterSet
    permission_classes = (permissions.IsAuthenticated, )
    queryset = QuerySet()
    serializer_class = LanguageSerializer

    def get_languages(
        self: Type,
    ) -> List[dict]:

        languages = []

        for code, name in settings.LANGUAGES_REGISTRY.languages.items():
            languages.append({
                'code': code,
                'name': name
            })

        return languages

    def list(
        self: Type,
        request: Type[Request],
    ) -> Type[Response]:

        languages = self.get_languages()

        data = {
            'next': None,
            'previous': None,
            'page': 1,
            'pages': 1,
            'total': len(languages),
            'results': self.serializer_class(languages, many=True).data
        }

        return Response(data)
