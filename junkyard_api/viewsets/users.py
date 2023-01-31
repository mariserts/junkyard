# -*- coding: utf-8 -*-
from typing import Final

from django.db.models.query import QuerySet

from rest_framework import mixins

from ..models import User
from ..serializers.users import UserSerializer

from .base import BaseViewSet


class UsersViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    BaseViewSet
):

    ordering_fields = ['id']
    queryset: Final = User.objects.all()
    serializer_class: Final = UserSerializer

    def get_queryset(
        self: BaseViewSet,
    ) -> QuerySet:

        queryset = self.queryset.filter(
            id=self.request.user.id
        ).order_by(
            *self.ordering_fields
        )

        return queryset
