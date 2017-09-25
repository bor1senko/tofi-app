# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from core.utils import send_mail
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError

import finance.api.accounts.serializers as serializers
import finance.models as fin_models
from core.api.generic.views import ModelViewSet, GenericViewSet
from jupiter_auth.authentication import TokenAuthentication
from jupiter_auth.utils import get_or_create_clients_group, get_or_create_admins_group


class AccountView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = fin_models.Account.objects.all()
    serializer_class = serializers.AccountSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        queryset = super(AccountView, self).get_queryset()
        if self.request.user.is_superuser:
            return queryset
        if get_or_create_admins_group() in self.request.user.groups.all():
            return queryset
        elif get_or_create_clients_group() in self.request.user.groups.all():
            statuses = [
                fin_models.Account.STATUS_ACTIVE,
                fin_models.Account.STATUS_DISABLED,
                fin_models.Account.STATUS_REQUESTED_CREATING
            ]
            return queryset.filter(client=self.request.user, status__in=statuses)
        else:
            return queryset.none()

    @list_route(methods=['POST'])
    def leave_create_claim(self, request, *args, **kwargs):
        """
        :param request:
        {
        }
        dummy - money from the wind
        admin can confirm it
        """
        first_contribution = 0
        client = request.user
        fin_models.Account.create(False, client, first_contribution)
        return Response('Заявка подана')

    @detail_route(methods=['POST'])
    def confirm_create_claim(self, request, *args, **kwargs):
        account = self.get_object()
        if account.status == account.STATUS_ACTIVE:
            raise ValidationError('Заявка на создание счета уже была обработана ранее.')
        if account.status != account.STATUS_REQUESTED_CREATING:
            raise ValidationError('Операции со счетом невозможны')
        else:
            if account.confirm():
                message = render_to_string('account/create_confirm_email.html')
                try:
                    send_mail('no-reply@jupiter-group.com', account.client.email,
                              'Ваша заявка на создание счета одобрена.', message)
                except Exception as e:
                    raise ValidationError('Ошибка при отправке письма: {}'.format(e))
                return Response('Создание счета подтверждено', status=status.HTTP_200_OK)
            raise ValidationError('Создание счета отклонено банком')

    @detail_route(methods=['POST'])
    def reject_create_claim(self, request, *args, **kwargs):
        """
        """
        account = self.get_object()
        cause = ''
        if account.status != account.STATUS_REQUESTED_CREATING:
            raise ValidationError('Заявка на создание счета была обработана ранее.')
        else:
            message = render_to_string('account/create_reject_email.html')
            try:
                send_mail('no-reply@jupiter-group.com', account.client.email,
                          'Ваша заявка на создание счета отклонена.', message)
            except Exception as e:
                raise ValidationError('Ошибка при отправке письма: {}'.format(e))
            account.reject(cause)
            return Response('Создание счета отклонено')

    @detail_route(methods=['POST'])
    def unassign(self, request, *args, **kwargs):
        account = self.get_object()
        if account.status == fin_models.Account.STATUS_REQUESTED_CREATING:
            account.delete()
            return Response('Заявка на открытие удалена')

        if account.status in account.INOPERABLE_STATUSES:
            raise ValidationError('Счет не может может быть закрыт.')
        if account.unassign():
            return Response('Заявка на закрытие отправлена.')
        else:
            raise ValidationError('Счет не может быть закрыт.')

    @list_route(methods=['POST'])
    def assign(self, request, *args, **kwargs):
        """
        :param request:
        {
            'account_number': 13digits
        }
        """
        self.serializer_class.assign_validate(request.data)
        client = request.user
        account_number = request.data['account_number']
        res, info = fin_models.Account.assign(client, account_number)
        return Response(info, status=status.HTTP_200_OK if res else status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['GET'])
    def info(self, request, *args, **kwargs):
        accounts = self.get_queryset()
        data = {
            "total_count": accounts.count(),
            "states_count": {
                str(status[0]): accounts.filter(status=status[0]).count()
                for status in fin_models.Account.STATUS_CHOICES
            }
        }
        return Response(data=data)