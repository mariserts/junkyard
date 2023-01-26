# -*- coding: utf-8 -*-
from typing import Final

from django.db.models.query import QuerySet

from rest_framework import mixins, viewsets

from ..models import User
from ..pagination import JunkyardApiPagination
from ..permissions import AuthenticatedUserPermission
from ..serializers.users import UserSerializer


class UsersViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    model: Final = User
    ordering_fields = ['id']
    pagination_class: Final = JunkyardApiPagination
    permission_classes: Final = (AuthenticatedUserPermission, )
    queryset: Final = model.objects.all()
    serializer_class: Final = UserSerializer

    def get_queryset(
        self: viewsets.GenericViewSet,
    ) -> QuerySet:

        queryset = self.queryset.filter(
            id=self.request.user.id
        ).order_by(
            *self.ordering_fields
        )

        return queryset
