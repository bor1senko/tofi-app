# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from hashlib import md5
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.utils import send_mail
from jupiter_auth.authentication import sign_in, sign_out, TokenAuthentication
from jupiter_auth.api.auth.serializers import SignInSerializer, SignUpSerializer
from jupiter_auth.api.auth.serializers import PasswordResetSerializer
from jupiter_auth.api.users.serializers import UserSerializer


class SignInView(CreateModelMixin, GenericViewSet):

    authentication_classes = ()
    serializer_class = SignInSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = sign_in(**serializer.validated_data)
        return Response({
            "token": token.key,
            "user": UserSerializer(user).data,
        }, status.HTTP_200_OK)


class SignOutView(ListModelMixin, GenericViewSet):

    authentication_classes = (TokenAuthentication,)

    def list(self, request, *args, **kwargs):
        sign_out(request.query_params.get('token'))
        return Response(status=status.HTTP_204_NO_CONTENT)


class SignUpView(CreateModelMixin, GenericViewSet):

    authentication_classes = ()
    serializer_class = SignUpSerializer


class PasswordResetView(GenericViewSet):

    authentication_classes = ()
    queryset = get_user_model().objects.all()
    serializer_class = PasswordResetSerializer

    @list_route(methods=['POST'])
    def reset(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = self.get_queryset().filter(email=email).first()
        if not user:
            raise ValidationError('Пользователь с указзанным email-ом не найдет')

        key = "{}:{}".format(md5(user.username).hexdigest(), user.pk)
        message = render_to_string('auth/password_reset_email.html', context={"key": key})
        try:
            send_mail('no-reply@jupiter-group.com', user.email, 'Восстановление пароля', message)
        except Exception as e:
            raise ValidationError('Ошибка при отправке письма: {}'.format(e))
        return Response(status=status.HTTP_200_OK)

    @list_route(methods=['POST'])
    def confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            key, pk = data['key'].rsplit(':', 1)
            user = self.get_queryset().get(pk=pk)
            assert md5(user.username).hexdigest() == key
        except (TypeError, AssertionError, ValueError, get_user_model().DoesNotExist) as e:
            raise ValidationError('Неверный ключ')

        if data['new_password'] != data['new_password_confirm']:
            raise ValidationError('Новые пароли не совпадают')

        user.set_password(data['new_password'])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)