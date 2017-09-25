# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import ValidationError
from core.utils import send_mail
from core.api.generic.views import ModelViewSet
from finance.models import Credit, Deposit, Transaction
from jupiter_auth.utils import get_or_create_clients_group, get_or_create_admins_group
from jupiter_auth.api.users.permissions import ManageSelfPermission
from jupiter_auth.api.users.serializers import (
    UserSerializer,
    ChangePasswordSerializer,
    CreateAdminSerializer
)


class UserView(ModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (ManageSelfPermission,)

    def get_queryset(self):
        queryset = super(UserView, self).get_queryset()
        if self.request.user.is_superuser:
            return queryset.filter(is_superuser=False)
        elif self.kwargs.get(self.lookup_field) == 'me':
            return queryset.filter(pk=self.request.user.pk)
        elif get_or_create_admins_group() in self.request.user.groups.all():
            return queryset.filter(groups=get_or_create_clients_group())
        else:
            return queryset.none()

    def get_object(self):
        if self.kwargs[self.lookup_field] == 'me':
            return self.request.user
        else:
            return super(UserView, self).get_object()

    @detail_route(methods=['GET'])
    def activate(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            raise ValidationError('Пользователь уже активирован')

        user.is_active = True
        user.save()

        message = render_to_string('auth/account_confirm_email.html')
        try:
            send_mail('no-reply@jupiter-group.com', user.email, 'Ваш аккаунт подтвержден', message)
        except Exception as e:
            raise ValidationError('Ошибка при отправке письма: {}'.format(e))
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['GET'])
    def deactivate(self, request, *args, **kwargs):
        user = self.get_object()
        if not user.is_active:
            raise ValidationError('Пользователь уже деактивирован')

        user.is_active = False
        user.save()

        message = render_to_string('auth/account_deactivate_email.html')
        try:
            send_mail('no-reply@jupiter-group.com', user.email, 'Ваш аккаунт отключен', message)
        except Exception as e:
            raise ValidationError('Ошибка при отправке письма: {}'.format(e))
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['GET'])
    def statistics(self, request, *args, **kwargs):
        client = self.get_object()
        client_credits = Credit.objects.filter(client=client)
        client_deposits = Deposit.objects.filter(client=client)
        client_transactions = Transaction.objects.filter(client=client)

        statistics = {
            "credits": {
                "total_count": client_credits.count(),
                "states_count": {
                    str(status[0]): client_credits.filter(status=status[0]).count()
                    for status in Credit.STATUS_CHOICES
                }
            },
            "deposits": {
                "total_count": client_deposits.count(),
                "states_count": {
                    str(status[0]): client_deposits.filter(status=status[0]).count()
                    for status in Deposit.STATUS_CHOICES
                }
            },
            "transactions": {
                "total_count": client_transactions.count(),
                "states_count": {
                    str(type[0]): client_transactions.filter(type=type[0]).count()
                    for type in Transaction.TYPES
                }
            }
        }
        return Response(data=statistics)

    @list_route(methods=['GET'])
    def info(self, request, *args, **kwargs):
        users = self.get_queryset()
        data = {
            "total_count": users.count(),
            "states_count": {
                "True": users.filter(is_active=True).count(),
                "False": users.filter(is_active=False).count(),
            }
        }
        return Response(data=data)

    @detail_route(methods=['POST'])
    def change_password(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = self.get_object()
        if not user.is_active:
            raise ValidationError('Пользователь деактивирован')
        if not user.check_password(serializer.validated_data['old_password']):
            raise ValidationError('Неверный пароль')
        if data['new_password'] != data['new_password_confirm']:
            raise ValidationError('Новые пароли не совпадают')

        user.set_password(data['new_password'])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=['POST'])
    def create_admin(self, request, *args, **kwargs):
        serializer = CreateAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
