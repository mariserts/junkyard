# -*- coding: utf-8 -*-
from typing import List, Union

from rest_framework import serializers
from rest_framework.reverse import reverse

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

    def to_representation(
        self: serializers.Serializer,
        instance: Union[Tenant, List[Tenant]]
    ) -> dict:

        many = True
        if type(instance) != list:
            many = False
            instance = [instance, ]

        output = []

        for object in instance:

            data = super(
                serializers.ModelSerializer,
                self
            ).to_representation(
                object
            )

            data['links'] = {
                'admins': reverse(
                    'admins-list',
                    args=[object.id],
                    request=self.context.get('request', None)
                ),
                'items': {
                    'all': reverse(
                        'items-list',
                        args=[object.id],
                        request=self.context.get('request', None)
                    ),
                },
            }

            types = settings.ITEM_TYPE_REGISTRY.get_type_names_as_list()

            for item_type in types:
                data['links']['items'][item_type] = reverse(
                    f'{item_type}-items-list',
                    args=[object.id],
                    request=self.context.get('request', None)
                )

            output.append(data)

        if many is True:
            return output

        return next(iter(output), None)

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
