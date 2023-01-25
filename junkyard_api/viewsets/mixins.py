import math

from typing import Union

from django.core.cache import cache
from django.db.models import Model
from django.db.models.query import QuerySet

from rest_framework.serializers import Serializer


class QuerySetMixin:

    def _get_object_or_404(self, model: Model, pk:str) -> Model:
        queryset = model.objects.all()
        object = get_object_or_404(queryset, pk=pk)
        return object


class CacheMixin:

    def _delete_cache(self, pk:str) -> None:
        cache_key = self._get_cache_key(pk)
        cache.delete(cache_key)

    def _get_cache_key(self, pk:str) -> str:
        return f'{self.cache_prefix}_{pk}'

    def _get_cached_data(self, pk:str) -> Union[dict, None]:
        cache_key = self._get_cache_key(pk)
        return cache.get(cache_key)

    def _set_cached_data(self, pk: str, data: dict) -> None:
        cache_key = self._get_cache_key(pk)
        cache.set(cache_key, data)


class PaginationMixin:

    def paginate(
        self,
        serializer: Serializer,
        queryset: QuerySet,
        page: int,
        count: int,
    ) -> dict:

        total = queryset.count()

        pages = math.ceil(total / count)
        if pages == 0:
            pages = 1

        start_from = (page - 1) * count

        skip_to = start_from + count

        queryset = queryset[start_from:skip_to]

        return {
            'page': page,
            'pages': pages,
            'results': serializer(queryset, many=True).data,
            'total': total,
        }
