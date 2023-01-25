from typing import Final, Union

from django.core.cache import cache
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Tenant
from ..serializers.tenants import TenantSerializer

from .mixins import CacheMixin, PaginationMixin, QuerySetMixin


class TenantsViewSet(
    CacheMixin,
    PaginationMixin,
    QuerySetMixin,
    viewsets.ViewSet
):

    cache_prefix: Final = 'tenants_'
    list_length = 10
    list_length_max = 500
    model = Tenant
    serializer = TenantSerializer

    def list(self, request: HttpRequest) -> Response:

        page = request.GET.get('page', '1')
        count = request.GET.get('count', str(self.list_length))
        owners = request.GET.getlist('owner', [])

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

        cleaned_owners = []
        for owner in owners:
            if owner.isdigit() is False:
                return Response('"owner" must be int', status=400)
            else:
                cleaned_owners.append(int(owner))

        # Base queryset

        queryset = self.model.objects.all()

        # Filter queryset

        if cleaned_owners != []:
            queryset = queryset.filter(owner_id__in=cleaned_owners)

        # Paginate

        data = self.paginate(self.serializer, queryset, page, count)

        if page > data['pages']:
            return Response(
                f'"page" {page} is not found',
                status=404
            )

        return Response(data, status=200)

    def create(self, request: HttpRequest) -> Response:

        if request.user.is_authenticated is False:
            return Response('Authentication required', status=403)

        if self.model.objects.filter(owner=request.user).exists():
            return Response('User already has 1 tenant', status=403)

        request_data = dict(request.data)
        request_data['owner'] = request.user.id

        # Validate data
        serializer = self.serializer(data=request_data)
        if serializer.is_valid() is False:
            return Response(
                {
                    'errors': serializer.errors,
                    'data': request_data
                },
                status=400
            )

        # Create object
        object = self.model.objects.create(**serializer.data)

        # Serialize new object
        serializer = self.serializer(object)

        data = serializer.data

        self._set_cached_data(object.id, data)

        return Response(data, status=201)

    def retrieve(self, request: HttpRequest, pk: str = None) -> Response:

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

        cached_data = self._get_cached_data(pk)
        if cached_data is None:
        	return Response('Not found!', status=404)

        if self._user_has_object_permission(pk, request.user.id) is False:
            return Response('Resource access denied!', status=403)

        # Find object
        object = self._get_object_or_404(self.model, pk)

        #
        request_data = dict(request.data)

        serializer = self.serializer(object, data=request_data)
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

        if self._user_has_object_permission(pk, request.user.id) is False:
            return Response('Resource access denied!', status=403)

        object = self._get_object_or_404(self.model, pk)
        object.delete()

        self._delete_cache(pk)

        return Response({'id': pk}, status=201)

    def _user_has_object_permission(self, pk, user_pk):
        return self.models.objects.filter(pk=pk, owner_id=user_pk).exists()
