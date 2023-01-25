from typing import Final, Union

from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from ..models import User
from ..serializers.users import UserSerializer

from .mixins import CacheMixin, PaginationMixin, QuerySetMixin


class UsersViewSet(
    CacheMixin,
    PaginationMixin,
    QuerySetMixin,
    viewsets.ViewSet
):

    cache_prefix: Final = 'users_'
    list_length = 10
    list_length_max = 500
    model = User
    serializer = UserSerializer

    # @action(detail=True, methods=['post'])
    # def change_password(self, request, pk=None):
    # pass

    # @action(detail=True, methods=['post'])
    # def change_email(self, request, pk=None):
    # pass

    # @action(detail=True, methods=['post'])
    # def request_password_reset_link(self, request, pk=None):
    # pass

    def list(self, request: HttpRequest) -> Response:

        if request.user.is_authenticated is False:
            return Response('Authentication required', status=403)

        emails = request.GET.getlist('email', [])
        page = request.GET.get('page', '1')
        count = request.GET.get('count', str(self.list_length))

        if page.isdigit() is False:
            return Response('"page" must be int', status=400)
        else:
            page = int(page)

        if page < 1:
            return Response('"page" must greater that 0', status=400)

        if count.isdigit() is False:
            return Response('"count" must be int', status=400)
        else:
            count = int(count)

        if count < 1:
            return Response(
                f'"count" min is 1',
                status=400
            )

        if count > self.list_length_max:
            return Response(
                f'"count" max is {self.list_length_max}',
                status=400
            )

        # Get base queryset

        queryset = self.model.objects.all()

        # Filter

        if emails != []:
            queryset = queryset.filter(email__in=emails)

        # Paginate

        data = self.paginate(self.serializer, queryset, page, count)

        if page > data['pages']:
            return Response(
                f'"page" {page} is not found',
                status=404
            )

        return Response(data, status=200)

    def create(self, request: HttpRequest) -> Response:

        request_data = dict(request.data)

        email = request_data['email']
        password = request_data.pop('password')

        if self.model.objects.filter(email=email).first() is not None:
            return Response(
                {
                    'errors': [
                        {'email': 'Email is taken'}
                    ],
                    'data': request_data
                },
                status=403
            )

        serializer = self.serializer(data=request.data)
        if serializer.is_valid() is False:
            return Response(
                {
                    'errors': serializer.errors,
                    'data': request_data
                },
                status=400
            )

        data = serializer.data

        object = self.model.objects.create(**data)

        object.set_password(password)
        object.save()

        serializer = self.serializer(object)

        data = serializer.data

        self._set_cached_data(object.id, data)

        return Response(data, status=201)

    def retrieve(self, request: HttpRequest, pk: str = None) -> Response:

        if request.user.is_authenticated is False:
            return Response('Authentication required', status=403)

        cached_data = self._get_cached_data(pk)
        if cached_data is not None:
            return Response(cached_data)

        object = self._get_object_or_404(self.model, pk)

        serializer = self.serializer(object)

        data = serializer.data

        self._set_cached_data(pk, data)

        return Response(data)

    def update(self, request: HttpRequest, pk: str = None) -> Response:

        if request.user.is_authenticated is False:
            return Response('Authentication required', status=403)

        if str(request.user.id) != pk:
            return Response('Resource access denied!', status=403)

        # Get object
        object = self._get_object_or_404(self.model, pk)

        #
        request_data = dict(request.data)

        # Form data allowed to change
        allowed_changes = {
            'first_name': request_data.get('first_name', ''),
            'last_name': request_data.get('last_name', '')
        }

        serializer = self.serializer(object, data=allowed_changes)
        if serializer.is_valid() is False:
            return Response(
                {
                    'errors': serializer.errors,
                    'data': request_data
                },
                status=400
            )

        serializer.save()

        data = serializer.data

        self._set_cached_data(pk, data)

        return Response(data, status=201)

    def delete(self, request: HttpRequest, pk: str = None) -> Response:

        if request.user.is_authenticated is False:
            return Response('Authentication required', status=403)

        if str(request.user.id) != pk:
            return Response('Resource access denied!', status=403)

        object = self._get_object_or_404(self.model, pk)
        object.delete()

        self._delete_cache(pk)

        return Response({'id': pk}, status=201)
