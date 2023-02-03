# -*- coding: utf-8 -*-
from typing import Final, List, Union

from django.db.models.query import QuerySet

from rest_framework.request import Request
from rest_framework.response import Response

from ..conf import settings
from ..filtersets.languages import LanguagesFilterSet
from ..serializers.languages import LanguageSerializer

from .base import BaseViewSet


class LanguagesViewSet(
    BaseViewSet
):

    filterset_class = LanguagesFilterSet
    serializer_class: Final = LanguageSerializer
    queryset = QuerySet()

    def get_languages(
        self: BaseViewSet,
    ) -> List[dict]:

        languages = settings.LANGUAGES

        languages = list(
            map(
                lambda language:
                    {
                        'code': language[0],
                        'name': language[1],
                        'default': language[0] == settings.LANGUAGE_DEFAULT
                    },
                languages
            )
        )

        return languages

    def get_language(
        self: BaseViewSet,
        code: str,
    ) -> dict:

        languages = self.get_languages()

        for language in languages:
            if language['code'] == code:
                return language

        return None

    def list(
        self: BaseViewSet,
        request: Request,
    ) -> Response:

        languages = self.get_languages()

        default = request.GET.get('default', None)

        if default in ['true', 'false', '1', '0']:
            default = default in ['true', '1']
        else:
            default = None

        if default is not None:
            languages = list(
                filter(
                    lambda language:
                        language['default'] == default,
                    languages
                )
            )

        data = {
            'next': None,
            'previous': None,
            'page': 1,
            'pages': 1,
            'total': len(languages),
            'results': self.serializer_class(languages, many=True).data
        }

        return Response(data)

    def retrieve(
        self: BaseViewSet,
        request: Request,
        pk: Union[None, str] = None
    ) -> Response:

        language = self.get_language(pk)
        if language is None:
            return Response('Not found', status=404)

        return Response(self.serializer_class(language).data)
