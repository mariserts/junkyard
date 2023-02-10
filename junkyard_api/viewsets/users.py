# -*- coding: utf-8 -*-
from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, viewsets

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
    ordering_fields = ('email', )
    pagination_class = JunkyardApiPagination
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer
