# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
from rest_framework.serializers import ModelSerializer, ValidationError
import finance.models as fin_models
from jupiter_auth.api.users.serializers import UserSerializer


class AccountSerializer(ModelSerializer):
    client = UserSerializer()

    class Meta:
        model = fin_models.Account

    @staticmethod
    def assign_validate(data):
        errors = {}
        number = data['account_number']
        if re.match('^3014\d{9}$', number) is None:
            errors['account_number'] = 'Номер расчетного счета для физ. лиц должен иметь формат 3014ЦЦЦЦЦЦЦЦЦ.'
        elif fin_models.Account.get_last_digit(number[:-1]) != number[-1]:
            errors['account_number'] = 'Допущена ошибка при наборе номера. ' \
                                       'Не пройдена проверка контрольной (последней цифры).'
        if len(errors) != 0:
            raise ValidationError(errors)
        return data