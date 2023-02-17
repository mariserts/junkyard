# -*- coding: utf-8 -*-
from rest_framework import serializers

from .base import BaseSerializer


class EmailSerializer(BaseSerializer):

    email = serializers.EmailField()


class EmailPasswordSerializer(BaseSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)


class EmailTokenPasswordSerializer(BaseSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)
    token = serializers.CharField()


class PasswordSerializer(BaseSerializer):

    password = serializers.CharField(min_length=8)


class TokenSerializer(BaseSerializer):

    token = serializers.CharField()
