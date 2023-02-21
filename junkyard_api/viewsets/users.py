# -*- coding: utf-8 -*-
from typing import List, Type

from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, viewsets
from rest_framework.response import Response

from ..filtersets.users import UsersFilterSet
from ..models import User
from ..pagination import JunkyardApiPagination
from ..serializers.users import UserSerializer


class UsersViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = UsersFilterSet
    ordering_fields = ['id', 'email', ]
    pagination_class = JunkyardApiPagination
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(
        self: Type,
        request: Type,
        *args: List,
        **kwargs: dict,
    ) -> Type[Response]:

        instance = self.get_object()

        serializer = self.get_serializer(instance)

        data = serializer.data
        data['permission_set'] = instance.permission_set.dict()

        return Response(data)
