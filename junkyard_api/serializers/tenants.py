# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..conf import settings
from ..models import Tenant


class TenantTranslatableContentSerializer(serializers.Serializer):

    language = serializers.ChoiceField(
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_DEFAULT
    )
    title = serializers.CharField()


class TenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tenant
        fields = '__all__'

    translatable_content = TenantTranslatableContentSerializer(many=True)
