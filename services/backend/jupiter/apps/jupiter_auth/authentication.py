# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError, AuthenticationFailed


def sign_in(username, password):
    user = get_user_model().objects.filter(username=username).first()
    if user and user.check_password(password):
        if not user.is_active:
            raise ValidationError('Ваш аккаунт еще не подтвержден')
        token, created = Token.objects.get_or_create(user=user)
        return user, token
    else:
        raise ValidationError('Incorrect username or password')


def sign_out(key):
    token = Token.objects.filter(key=key).first()
    if token:
        token.delete()
    else:
        raise AuthenticationFailed('Incorrect token')


def get_token(request):
    return request.query_params.get('token')


class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        key = get_token(request)
        try:
            token = Token.objects.select_related('user').get(key=key)
            if not token.user:
                raise AuthenticationFailed('Incorrect token')
            return token.user, token
        except Token.DoesNotExist:
            raise AuthenticationFailed('Incorrect token')
