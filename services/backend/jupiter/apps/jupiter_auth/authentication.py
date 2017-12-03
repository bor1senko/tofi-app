# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


from jupiter_auth.models import ServiceAddOn

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

    backends = ['authenticateToken', 'authenticateService']

    def authenticateService(self, request):
        key = get_token(request)
        try:
            service = ServiceAddOn.objects.get(token=key)
            if not service:
                raise Exception('Incorrect token2')
            return service, None
        except ServiceAddOn.DoesNotExist:
            raise Exception('Incorrect token2')

    def authenticateToken(self, request):
        key = get_token(request)
        try:
            token = Token.objects.select_related('user').get(key=key)
            if not token.user:
                raise Exception('Incorrect token1')
            return token.user, token
        except Token.DoesNotExist:
            raise Exception('Incorrect token1')

    def authenticate(self, request):
        for auth_name in self.backends:
            auth_func = getattr(self, auth_name, None)
            if auth_func:
                try:
                    return auth_func(request)
                except Exception as e:
                    continue
            raise AuthenticationFailed('Incorrect token')
