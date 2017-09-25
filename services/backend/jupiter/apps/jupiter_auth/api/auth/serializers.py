# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers
from django.contrib.auth import get_user_model
from jupiter_auth.utils import get_or_create_clients_group
from jupiter_auth.api.users.serializers import UserProfileSerializer
from jupiter_auth.models import UserProfile


class SignInSerializer(serializers.ModelSerializer):

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class SignUpSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)

    def create(self, validated_data):
        validated_data['is_active'] = False
        profile_data = validated_data.pop('profile')
        instance = get_user_model().objects.create_user(**validated_data)
        instance.groups.add(get_or_create_clients_group())
        UserProfile.objects.create(user=instance, **profile_data)
        return instance

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'password',
            'email',
            'profile',
            'first_name',
            'last_name',
        )


class PasswordResetSerializer(serializers.Serializer):

    key = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_confirm = serializers.CharField(required=True, write_only=True)