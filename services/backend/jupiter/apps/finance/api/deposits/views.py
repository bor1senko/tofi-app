# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from core.utils import send_mail
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError

import finance.models as fin_models
import finance.api.deposits.serializers as serializers
from jupiter_auth.authentication import TokenAuthentication
from core.api.generic.views import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from jupiter_auth.utils import get_or_create_clients_group, get_or_create_admins_group


class DepositView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = fin_models.Deposit.objects.all()
    serializer_class = serializers.DepositSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        queryset = super(DepositView, self).get_queryset()
        if self.request.user.is_superuser:
            return queryset
        if get_or_create_admins_group() in self.request.user.groups.all():
            return queryset
        elif get_or_create_clients_group() in self.request.user.groups.all():
            return queryset.filter(client=self.request.user)
        else:
            return queryset.none()

    @list_route(methods=['POST'])
    def leave_create_claim(self, request, *args, **kwargs):
        """
        :param request:
        {
            "template_id": id
            "amount": money_amount, in BYN
            "duration": duration,
            "percentage": percentage (0...100),
            "currency": currency,
            "account_id": source_account_id,
        }
        admin can confirm it
        """
        money_amount = request.data['amount']
        client = request.user
        template = fin_models.DepositTemplate.objects.get(pk=request.data['template_id'])
        duration = request.data['duration']
        percentage = request.data['percentage']
        currency = request.data['currency']
        account_id = request.data['account_id']
        if not fin_models.Account.objects.filter(pk=account_id):
            raise ValidationError('Указанного счета не существует.')

        account = fin_models.Account.objects.get(pk=account_id)
        if account.status in fin_models.Account.INOPERABLE_STATUSES:
            raise ValidationError('Операции с указанным счетом невозможны.')

        deposit = fin_models.Deposit.create(
            client, template, money_amount, duration,
            percentage, currency, account_id
        )
        if deposit is None:
            raise ValidationError('На указаном счете недостаточно денег')
        else:
            return Response('Заявка подана. Указанный счет временно заморожен.')

    @detail_route(methods=['PATCH'])
    def confirm_create_claim(self, request, *args, **kwargs):
        deposit = self.get_object()
        if deposit.status != deposit.STATUS_REQUESTED_CREATING:
            raise ValidationError('Заявка на создание депозита уже была обработана.')
        else:
            if deposit.confirm():
                message = render_to_string('deposit/create_confirm_email.html')
                try:
                    send_mail('no-reply@jupiter-group.com', deposit.client.email,
                              'Ваша заявка на создание депозита одобрена.', message)
                except Exception as e:
                    raise ValidationError('Ошибка при отправке письма: {}'.format(e))
                return Response('Создание депозита подтверждено', status=status.HTTP_200_OK)
            else:
                raise ValidationError('Отклонено банком.')

    @detail_route(methods=['PATCH'])
    def reject_create_claim(self, request, *args, **kwargs):
        """
        :param request:
        {
            "cause", cause of rejection
        }
        """
        deposit = self.get_object()
        cause = request.data['cause']
        if deposit.status != deposit.STATUS_REQUESTED_CREATING:
            raise ValidationError('Заявка на создание депозита уже была обработана.')
        else:
            message = render_to_string('deposit/create_reject_email.html')
            try:
                send_mail('no-reply@jupiter-group.com', deposit.client.email,
                          'Ваша заявка на создание депозита отклонена.', message)
            except Exception as e:
                raise ValidationError('Ошибка при отправке письма: {}'.format(e))
            deposit.reject(cause)
            return Response('Создание депозита отклонено')

    @detail_route(methods=['PATCH'])
    def leave_close_claim(self, request, *args, **kwargs):
        """
        :param request:
        {
            "target_account_id": account_id
        }
        """
        deposit = self.get_object()
        if deposit.status in deposit.INOPERABLE_STATUSES:
            raise ValidationError('Операции с депозитом невозможны')
        if deposit.status == deposit.STATUS_REQUESTED_CLOSING:
            raise ValidationError('Заявка на закрытие депозита уже подана.')

        target_account_id = request.data['target_account_id']
        if not fin_models.Account.objects.filter(pk=target_account_id):
            raise ValidationError('Указанного счета не существует.')
        account = fin_models.Account.objects.get(pk=target_account_id)
        if account.status in fin_models.Account.INOPERABLE_STATUSES:
            raise ValidationError('Операции с указанным счетом невозможны.')
        res, info = deposit.leave_close_claim(target_account_id)
        return Response(info, status=status.HTTP_200_OK if res else status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['PATCH'])
    def confirm_close_claim(self, request, *args, **kwargs):
        deposit = self.get_object()
        if deposit.status != deposit.STATUS_REQUESTED_CLOSING:
            raise ValidationError('Заявка на закрытие депозита не подана.')
        if deposit.close_confirm():
            message = render_to_string('deposit/create_confirm_email.html')
            try:
                send_mail('no-reply@jupiter-group.com', deposit.client.email,
                          'Ваша заявка на закрытие депозита одобрена.', message)
            except Exception as e:
                raise ValidationError('Ошибка при отправке письма: {}'.format(e))
            return Response('Закрытие подтверждено, деньги переведены.', status=status.HTTP_200_OK)
        else:
            raise ValidationError('Заявка на закрытие не была подана.')

    @detail_route(methods=['PATCH'])
    def reject_close_claim(self, request, *args, **kwargs):
        """
        :param request:
        {
            "cause", cause of rejection
        }
        """
        deposit = self.get_object()
        if deposit.status != deposit.STATUS_REQUESTED_CLOSING:
            raise ValidationError('Заявка на закрытие депозита не подана.')
        cause = request.data['cause']
        if deposit.close_reject(cause):
            message = render_to_string('deposit/close_reject_email.html')
            try:
                send_mail('no-reply@jupiter-group.com', deposit.client.email,
                          'Ваша заявка на закрытие депозита отклонена.', message)
            except Exception as e:
                raise ValidationError('Ошибка при отправке письма: {}'.format(e))
            return Response('Закрытие отклонено.', status=status.HTTP_200_OK)
        else:
            raise ValidationError('Заявка на закрытие не была подана.')

    @detail_route(methods=['POST'])
    def put_money(self, request, *args, **kwargs):
        """
        :param request:
        {
            "amount": money_amount (in BLR - only in BLR),
            "account_id": account_id (get money from account)
        Add money to deposit
        """
        deposit = self.get_object()
        if deposit.status != deposit.STATUS_ACTIVE:
            raise ValidationError('Операции с депозитом невозможны')
        if not deposit.additional_contributions:
            raise ValidationError('Данный депозит не позволяет дополнительных начислений.')

        amount = request.data['amount']
        account_id = request.data["account_id"]
        if not fin_models.Account.objects.filter(pk=account_id):
            raise ValidationError('Указанного счета не существует.')

        account = fin_models.Account.objects.get(pk=account_id)
        if request.user != account.client:
            raise ValidationError('Невозможно использование чужого счета.')
        if account.status in fin_models.Account.INOPERABLE_STATUSES:
            raise ValidationError('Операции с указанным счетом невозможны.')

        if account.get_money(amount):
            if deposit.additional_contribution(amount):
                deposit.save()
                return Response('Дополнительные средства перечислены.')
            else:
                account.put_money(amount)
                raise ValidationError('Отклонено банком. Ваш счет не подтвержден или не активен.')
        else:
            raise ValidationError('Недостаточно средств на счете')

    @list_route(methods=['GET'])
    def info(self, request, *args, **kwargs):
        deposits = self.get_queryset()
        data = {
            "total_count": deposits.count(),
            "states_count": {
                str(status[0]): deposits.filter(status=status[0]).count()
                for status in fin_models.Deposit.STATUS_CHOICES
            }
        }
        return Response(data=data)


class DepositTemplateView(ReadOnlyModelViewSet):
    queryset = fin_models.DepositTemplate.objects.all()
    serializer_class = serializers.DepositTemplateSerializer
