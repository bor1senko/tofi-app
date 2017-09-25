# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
import finance.models as fin_models
from jupiter_auth.api.users.serializers import UserSerializer


class CreditTemplateSerializer(ModelSerializer):
    class Meta:
        model = fin_models.CreditTemplate


class CreditSerializer(ModelSerializer):

    client = UserSerializer()
    template = CreditTemplateSerializer()
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return (obj.residue + obj.current_penalty + obj.current_month_percents).amount

    class Meta:
        model = fin_models.Credit

    @staticmethod
    def leave_create_claim_validate(value):
        """
        {
            "template_id": id,
            "amount": money_amount, in BYN,
            "duration": duration,
            "ensuring_method": ensuring_method,
            "money_destination": dest,
            "account_id": target_account_id
        }
        """
        errors = {}
        template = fin_models.CreditTemplate.objects.get(pk=value['template_id'])
        min_amount = template.min_amount['fixed']
        max_amount = template.max_amount['fixed']
        min_duration = 1
        max_duration = template.max_duration
        amount = value['amount']
        duration = value['duration']
        account_id = value['account_id']
        account_number = fin_models.Account.objects.get(pk=account_id).number
        if template.type == template.TYPE_SELLER:
            if re.match('^301(2|3|4|5)\d{9}$', account_number) is None:
                errors['account_id'] = 'Номер расчетного счета должен иметь формат 301(2,3,4)ЦЦЦЦЦЦЦЦЦ ' \
                                       'для коммерческих орг., ИП, физ. лиц. соответственно.'
        else:
            if re.match('^3014\d{9}$', account_number) is None:
                errors['account_id'] = 'Номер расчетного счета физ. лица должен иметь формат 3014ЦЦЦЦЦЦЦЦЦ.'
        if not (min_amount <= amount <= max_amount):
            errors['amount'] = 'Допустимая сумма: от {} BYN до {} BYN.'.format(min_amount, max_amount)
        if not (min_duration <= duration <= max_duration):
            errors['duration'] = 'Допустимый срок: от {} до {} месяцев.'.format(min_duration, max_duration)
        if len(errors):
            raise ValidationError(errors)
        return value