# -*- coding: utf-8 -*-
from typing import Type

from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, viewsets

from ..filtersets.item_relations import ItemRelationsFilterSet
from ..models import ItemRelation, User
from ..pagination import JunkyardApiPagination
from ..serializers.item_relations import ItemRelationSerializer


class ItemRelationsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ItemRelationsFilterSet
    ordering_fields = ('id', )
    pagination_class = JunkyardApiPagination
    permission_classes = (permissions.IsAuthenticated, )
    queryset = ItemRelation.objects.all()
    serializer_class = ItemRelationSerializer

    def get_queryset(
        self: Type,
    ) -> QuerySet:

        if self.request.user.is_authenticated is False:
            return ItemRelation.objects.none()

        item_pk = self.kwargs.get('item_pk', '-1')
        tenant_ids = User.get_tenants(self.request.user, format='ids')

        queryset = self.queryset.filter(
            child_id=item_pk,
            child__tenant_id__in=tenant_ids,
        ).select_related(
            'child'
        ).order_by(
            *self.ordering_fields
        )

        return queryset
