# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..conf import settings
from ..models import Item


class ItemSerializer(serializers.ModelSerializer):

    item_type = serializers.ChoiceField(choices=())

    class Meta:
        model = Item
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super(ItemSerializer, self).__init__(*args, **kwargs)

        field = self.fields['item_type']
        field.choices = settings.ITEM_TYPE_REGISTRY.get_types_as_choices()
