from typing import Final, Union

from django.core.cache import cache
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from ..conf import settings
from ..models import Item, Tenant
from ..serializers.items import ItemSerializer

from .mixins import CacheMixin, PaginationMixin, QuerySetMixin


class ItemsViewSet(
    CacheMixin,
    PaginationMixin,
    QuerySetMixin,
    viewsets.ViewSet
):

    cache_prefix: Final = 'items_'
    list_length = 10
    list_length_max = 500
    model = Item
    serializer = ItemSerializer

    # @action(detail=True, methods=['post'])
    # def publish(self, request, pk):
    #     pass

    # @action(detail=True, methods=['post'])
    # def unpublish(self, request, pk):
    #     pass

    def list(self, request: HttpRequest) -> Response:

        page = request.GET.get('page', '1')
        count = request.GET.get('count', str(self.list_length))
        tenants = request.GET.getlist('tenant', [])

        # Clean data

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

        cleaned_tenants = []
        for tenant in tenants:
            if tenant.isdigit() is False:
                return Response('"tenant" must be int', status=400)
            else:
                cleaned_tenants.append(int(tenant))

        # Get base queryset

        queryset = self.model.objects.all()

        # Filter queryset

        if cleaned_tenants != []:
            queryset = queryset.filter(tenant_id__in=cleaned_tenants)

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

        request_data = dict(request.data)

        try:
            tenant_pk = request_data['tenant']
        except KeyError:
            return Response(
                {
                    'errors': {
                        'tenant': 'Tenant is required in payload'
                    },
                    'data': request_data
                },
                status=400
            )

        user_pk = request.user.id

        try:
            item_type = request_data['item_type']
        except KeyError:
            return Response(
                {
                    'errors': {
                        'tenant': 'Item type is required in payload'
                    },
                    'data': request_data
                },
                status=400
            )

        # Check if user can create items for item tenant
        if self._user_has_tenant_permission(tenant_pk, user_pk) is False:
            return Response('Resource access denied', status=403)

        # Get specific serializer
        registered_serializer = settings.ITEM_TYPE_REGISTRY.find(item_type)
        if registered_serializer is None:
            return Response(
                {
                    'errors': {
                        'item_type': f'Item type "{item_type}" not found'
                    },
                    'data': request_data
                },
                status=400
            )

        # Serialize data
        serializer = registered_serializer(data=request_data)
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

        item_type = object.item_type

        # Get specific serializer
        registered_serializer = settings.ITEM_TYPE_REGISTRY.find(item_type)
        if registered_serializer is None:
            serializer = self.serializer(object)
        else:
            serializer = registered_serializer(object)

        #
        data = serializer.data

        # Cache result
        self._set_cached_data(pk, data)

        return Response(data)

    def update(self, request: HttpRequest, pk: str = None) -> Response:

        if request.user.is_authenticated is False:
            return Response('Authentication required', status=403)

        cached_data = self._get_cached_data(self.model, pk)
        if cached_data is None:
        	return Response('Not found!', status=404)

        if self._user_has_object_permission(pk, request.user.id) is False:
            return Response('Resource access denied', status=403)

        # Check if user can update items for item tenant

        # Find object
        object = self._get_object_or_404(pk)

        #
        request_data = dict(request.data)

        request_data['id'] = object.id
        request_data['tenant'] = object.tenant_id
        request_data['item_type'] = object.item_type

        # Get item type
        item_type = object.item_type

        #  Get specific serializer
        registered_serializer = settings.ITEM_TYPE_REGISTRY.find(item_type)
        if registered_serializer is None:
            return Response(
                {
                    'errors': {
                        'item_type': f'Item type "{item_type}" not found'
                    },
                    'data': request_data
                },
                status=400
            )

        # Serializer
        serializer = registered_serializer(object, data=request_data)
        if serializer.is_valid() is False:
            return Response(
                {
                    'errors': serializer.errors,
                    'data': request_data
                },
                status=400
            )

        #
        serializer.save()

        #
        data = serializer.data

        # Set new cache
        self._set_cached_data(pk, data)

        return Response(data, status=201)

    def delete(self, request: HttpRequest, pk: str = None) -> Response:

        if request.user.is_authenticated is False:
            return Response('Authentication required', status=403)

        if self._user_has_object_permission(pk, request.user.id) is False:
            return Response('Resource access denied', status=403)

        object = self._get_object_or_404(self.model, pk)
        object.delete()

        self._delete_cache(pk)

        return Response({'id': pk}, status=201)

    def _user_has_object_permission(self, pk, user_pk):
        return self.model.objects.filter(
            pk=pk,
            tenant__owner_id=user_pk
        ).exists()

    def _user_has_tenant_permission(self, pk, user_pk):
        return Tenant.objects.filter(
            pk=pk,
            owner_id=user_pk
        ).exists()
