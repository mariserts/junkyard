# -*- coding: utf-8 -*-
from rest_framework import serializers

from .items import ItemSerializer


class ProjectsTenantsItemsSerializer(ItemSerializer):

    tenant_id = serializers.IntegerField()
