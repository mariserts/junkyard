# -*- coding: utf-8 -*-
from junkyard_api.filtersets.external_filterset import ExternalFilterSet

from .conf import settings


class NewsFilterSet(ExternalFilterSet):

    item_type = settings.ITEM_TYPE
