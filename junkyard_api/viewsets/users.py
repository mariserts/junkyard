# -*- coding: utf-8 -*-
from typing import Final

from django.db.models.query import QuerySet

from rest_framework import mixins, permissions

from ..filtersets.users import UsersFilterSet
from ..models import User
from ..permissions import AuthenticatedOrUnAuthenticatedCreate
from ..serializers.users import UserSerializer

from .base import BaseViewSet


class UsersViewSet(
    # mixins.CreateModelMixin,
    # mixins.DestroyModelMixin,
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

    # def create(self, request, *args, **kwargs):
    #
    #     try:
    #         email = request.data['email']
    #     except KeyError:
    #         raise serializers.ValidationError({
    #             'email': ['email is required']
    #         })
    #
    #     try:
    #         password = request.data['password']
    #     except KeyError:
    #         raise serializers.ValidationError({
    #             'password': ['password is required']
    #         })
    #
    #     try:
    #         validate_email(email)
    #     except ValidationError:
    #         raise serializers.ValidationError({
    #             'email': ['Email is invalid']
    #         })
    #
    #     try:
    #         validate_password(password)
    #     except ValidationError as e:
    #         raise serializers.ValidationError({
    #             'password': [str(e)]
    #         })
    #
    #     exists = User.objects.filter(email=email).exists()
    #     if exists is True:
    #         raise serializers.ValidationError({
    #             'email': ['Email is taken']
    #         })
    #
    #     user = User.objects.create_user(
    #         email=email,
    #         password=password
    #     )
    #
    #     return Response(
    #         UserSerializer(user).data,
    #         status=201
    #     )

    # @action(
    #     detail=True,
    #     methods=['post'],
    #     name='Change Password',
    #     url_path='set-password',
    # )
    # def set_password(self, request, pk=None):
    #
    #     if str(pk) != str(request.user.id):
    #         return Response('Permission denied', status=403)
    #
    #     try:
    #         password = request.data['password']
    #     except KeyError:
    #         raise serializers.ValidationError({
    #             'password': ['password is required']
    #         })
    #
    #     try:
    #         validate_password(password)
    #     except ValidationError as e:
    #         raise serializers.ValidationError({
    #             'password': [str(e)]
    #         })
    #
    #     request.user.set_password(password)
    #
    #     return Response(
    #         {},
    #         status=200
    #     )
