# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers
from rest_framework.serializers import Serializer


class FieldInfoSerializer(Serializer):

    required = serializers.BooleanField(read_only=True)
    allow_null = serializers.BooleanField(read_only=True)
    unique = serializers.BooleanField(read_only=True)
    type = serializers.SerializerMethodField(method_name='_get_type')

    @staticmethod
    def _get_type(instance):
        return instance.__class__.__name__

    def to_representation(self, instance):
        data = super(FieldInfoSerializer, self).to_representation(instance[1])
        data.update({"name": instance[0]})
        return data
