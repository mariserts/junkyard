from typing import Final, Union

from django.core.cache import cache
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from ..models import User
from ..serializers.users import UserSerializer


class IdentityViewSet(
    viewsets.ViewSet
):

    model = User
    serializer = UserSerializer

    # @action(detail=True, methods=['post'])
    # def sign_in(self, request, pk=None):
    # pass

    # @action(detail=True, methods=['post'])
    # def sign_out(self, request, pk=None):
    # pass

    # @action(detail=True, methods=['post'])
    # def reset_password(self, request, pk=None):
    # pass

    # @action(detail=True, methods=['post'])
    # def request_password_reset_link(self, request, pk=None):
    # pass
