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

    def validate_translatable_content(self, data):

        count = len(data)

        if count == 1:
            return data

        if count == 0:
            raise serializers.ValidationError(
                'At least 1 translatable content required'
            )

        languages = []
        for content in data:
            languages.append(content['language'])

        if len(list(set(languages))) != count:
            raise serializers.ValidationError(
                'Content languages are not unique'
            )

        if settings.LANGUAGE_DEFAULT not in languages:
            raise serializers.ValidationError(
                'Default language content is missing'
            )

        return data
