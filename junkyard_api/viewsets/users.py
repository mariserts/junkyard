# -*- coding: utf-8 -*-
from typing import Final

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models.query import QuerySet

from rest_framework import mixins, permissions, serializers
from rest_framework.response import Response

from ..filtersets.users import UsersFilterSet
from ..models import User
from ..permissions import AuthenticatedOrUnAuthenticatedCreate
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

    filterset_class: Final = UsersFilterSet
    ordering_fields: Final = ('id', )
    permission_classes: Final = (AuthenticatedOrUnAuthenticatedCreate, )
    queryset: Final = User.objects.all()
    serializer_class: Final = UserSerializer

    def get_queryset(
        self: BaseViewSet,
    ) -> QuerySet:

        queryset = self.queryset.filter(
            is_active=True
        )

        if self.request.method not in permissions.SAFE_METHODS:
            queryset = queryset.filter(
                id=self.request.user.id,
            )

        queryset = queryset.order_by(
            *self.ordering_fields
        )

        return queryset

    def create(self, request, *args, **kwargs):

        email = request.data['email']
        password = request.data['password']

        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError({
                'email': ['Email is malformed']
            })

        try:
            validate_password(password)
        except ValidationError:
            raise serializers.ValidationError({
                'password': ['Password is too weak']
            })

        exists = User.objects.filter(email=email).exists()
        if exists is True:
            raise serializers.ValidationError({
                'email': ['Email is taken']
            })

        user = User.objects.create_user(
            email=email,
            password=password
        )

        return Response(
            UserSerializer(user).data,
            status=201
        )
