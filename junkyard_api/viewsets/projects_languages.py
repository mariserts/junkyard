# -*- coding: utf-8 -*-
from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from rest_framework import permissions, mixins, viewsets

from ..filtersets.languages import LanguagesFilterSet
from ..serializers.languages import LanguageSerializer


class ProjectsLanguagesViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = LanguagesFilterSet
    # ordering_fields = ('name', )
    permission_classes = (permissions.IsAuthenticated, )
    queryset = QuerySet()
    serializer_class = LanguageSerializer
