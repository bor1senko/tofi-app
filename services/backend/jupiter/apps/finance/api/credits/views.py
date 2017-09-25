# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin

from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from core.api.generic.views import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.exceptions import ValidationError
from core.utils import send_mail
from django.template.loader import render_to_string

import finance.models as fin_models
import finance.api.credits.serializers as serializers
from core.api.generic.views import ModelViewSet, ReadOnlyModelViewSet
from jupiter_auth.authentication import TokenAuthentication
from jupiter_auth.utils import get_or_create_clients_group, get_or_create_admins_group


class CreditView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = fin_models.Credit.objects.all()
    serializer_class = serializers.CreditSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        queryset = super(CreditView, self).get_queryset()
        if self.request.user.is_superuser:
            return queryset
        if get_or_create_admins_group() in self.request.user.groups.all():
            return queryset
        elif get_or_create_clients_group() in self.request.user.groups.all():
            return queryset.filter(client=self.request.user)
        else:
            return queryset.none()

    @detail_route(methods=['POST'])
    def make_payment(self, request, *args, **kwargs):
        """
        Pay on the loan from client account
        :param request:
        {
            "amount": money_amount (only in BLR),
            "account_id": account_id (get money from account)
        }
        """
        credit = self.get_object()
        amount = request.data['amount']
        account_id = request.data["account_id"]

        try:
            amount = float(amount)
        except Exception as e:
            raise ValidationError('Сумма должна быть числом')

        if credit.status in fin_models.Credit.INOPERABLE_STATUSES:
            raise ValidationError('Операции с кредитом невозможны.')
        if not fin_models.Account.objects.filter(pk=account_id):
            raise ValidationError('Указанного счета не существует.')

        account = fin_models.Account.objects.get(pk=account_id)
        if request.user != account.client:
            raise ValidationError('Вы не можете использовать чужой расчетный счет.')
        if account.status in fin_models.Account.INOPERABLE_STATUSES:
            return Response('Операции с указанным счетом невозможны.', status=status.HTTP_400_BAD_REQUEST)

        if account.get_money(amount):
            if credit.pay(amount):
                credit.save()
                return Response('Оплачено.')
            else:
                account.put_money(amount)
                raise ValidationError('Отклонено банком. Ваш счет не подтвержден или не активен.')
        else:
            raise ValidationError('Недостаточно средств на счете')

    @list_route(methods=['POST'])
    def open_online(self, request, *args, **kwargs):
        """
        client, template, money_amount, duration, account_id=None
        :param request:
        {
            "template_id": id,
            "amount": money_amount, id,
            "duration": duration in months,
            "account_id": account_id
        }
        """
        client = request.user
        money_amount = request.data['amount']
        template = fin_models.CreditTemplate.objects.get(pk=request.data['template_id'])
        duration = request.data['duration']
        account_id = request.data['account_id']
        if not fin_models.Account.objects.filter(pk=account_id):
            raise ValidationError('Указанного счета не существует.')

        account = fin_models.Account.objects.get(pk=account_id)
        if account.status in fin_models.Account.INOPERABLE_STATUSES:
            raise ValidationError('Операции с указанным счетом невозможны.')
        if not template.issue_online:
            raise ValidationError('Данный кредит нельзя открыть онлайн')

        self.serializer_class.leave_create_claim_validate(request.data)
        res = fin_models.Credit.create_online(
            client, template, money_amount, duration, account_id
        )
        info = 'Экспресс кредит открыт' if res[0] else res[1]
        return Response(info, status=status.HTTP_200_OK if res[0] else status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def leave_create_claim(self, request, *args, **kwargs):
        """
        :param request:
        {
            "template_id": id,
            "amount": money_amount, in BYN,
            "duration": duration,
            "ensuring_method": ensuring_method,
            "money_destination": dest,
            "account_id": target_account_id
        }
        admin can confirm it
        """
        money_amount = request.data['amount']
        client = request.user
        template = fin_models.CreditTemplate.objects.get(pk=request.data['template_id'])
        duration = request.data['duration']
        ensuring_method = request.data['ensuring_method']
        money_destination = request.data['money_destination']
        account_id = request.data['account_id']
        if not fin_models.Account.objects.filter(pk=account_id):
            raise ValidationError('Указанного счета не существует.')

        account = fin_models.Account.objects.get(pk=account_id)
        if account.status in fin_models.Account.INOPERABLE_STATUSES:
            raise ValidationError('Операции с указанным счетом невозможны.')

        self.serializer_class.leave_create_claim_validate(request.data)
        fin_models.Credit.create_claim(
            client, template, money_amount, duration,
            ensuring_method, money_destination, account_id
        )
        return Response('Заявка подана')

    @detail_route(methods=['PATCH'])
    def confirm_create_claim(self, request, *args, **kwargs):
        credit = self.get_object()
        if credit.status != credit.STATUS_REQUESTED:
            raise ValidationError('Заявка на создание кредита была обработана ранее.')
        else:
            if credit.confirm():
                message = render_to_string('credit/create_confirm_email.html')
                try:
                    send_mail('no-reply@jupiter-group.com', credit.client.email,
                              'Ваша заявка на создание кредита одобрена.', message)
                except Exception as e:
                    raise ValidationError('Ошибка при отправке письма: {}'.format(e))
                return Response('Создание кредита подтверждено', status=status.HTTP_200_OK)
            else:
                raise ValidationError('Отклонено банком')

    @detail_route(methods=['PATCH'])
    def reject_create_claim(self, request, *args, **kwargs):
        """
        :param request:
        {
            "cause", cause of rejection
        }
        """
        credit = self.get_object()
        cause = request.data['cause']
        if credit.status != credit.STATUS_REQUESTED:
            raise ValidationError('Заявка на создание кредита была обработана ранее.')
        else:
            message = render_to_string('credit/create_reject_email.html')
            try:
                send_mail('no-reply@jupiter-group.com', credit.client.email,
                          'Ваша заявка на создание кредита отклонена.', message)
            except Exception as e:
                raise ValidationError('Ошибка при отправке письма: {}'.format(e))
            credit.reject(cause)
            return Response('Создание кредита отклонено')

    @detail_route(methods=['PATCH'])
    def close(self, request, *args, **kwargs):
        """
        User can close credit without confirmation
        """
        credit = self.get_object()
        if credit.status in fin_models.Credit.INOPERABLE_STATUSES:
            raise ValidationError('Операции с кредитом невозможны.')
        if credit.close():
            return Response('Кредит закрыт', status=status.HTTP_200_OK)
        else:
            raise ValidationError('Кредит не выплачен. погасите задолженность.')

    @list_route(methods=['GET'])
    def info(self, request, *args, **kwargs):
        credits = self.get_queryset()
        data = {
            "total_count": credits.count(),
            "states_count": {
                str(status[0]): credits.filter(status=status[0]).count()
                for status in fin_models.Credit.STATUS_CHOICES
            }
        }
        return Response(data=data)


class CreditTemplateView(ReadOnlyModelViewSet):
    queryset = fin_models.CreditTemplate.objects.all()
    serializer_class = serializers.CreditTemplateSerializer
