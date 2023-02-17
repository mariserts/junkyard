# -*- coding: utf-8 -*-
from .base import BaseItemTypeSerializer, BaseProjectSerializer


class ProjectSerializer(BaseProjectSerializer):

    item_types_for_project = BaseItemTypeSerializer(many=True, read_only=True)
    item_types_for_tenants = BaseItemTypeSerializer(many=True, read_only=True)
