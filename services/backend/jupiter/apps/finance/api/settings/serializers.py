# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from finance.models import FinanceSettings


class FinanceSettingsSerializer(serializers.ModelSerializer):

    scoring = serializers.DictField(required=True)
    currencies = serializers.ListField(read_only=True)
    exchange_rates = serializers.DictField(read_only=True)

    def validate(self, attrs):
        attrs = super(FinanceSettingsSerializer, self).validate(attrs)
        scoring_settings = attrs['scoring']
        if 'warning_level' not in scoring_settings:
            raise ValidationError({'warning_level': 'Это поле обязательное'})
        if 'danger_level' not in scoring_settings:
            raise ValidationError({'danger_level': 'Это поле обязательное'})

        try:
            scoring_settings['warning_level'] = float(scoring_settings['warning_level'])
        except Exception:
            raise ValidationError({'warning_level': 'Число в неверном формате'})

        try:
            scoring_settings['danger_level'] = float(scoring_settings['danger_level'])
        except Exception:
            raise ValidationError({'danger_level': 'Число в неверном формате'})

        if scoring_settings['warning_level'] <= scoring_settings['danger_level']:
            raise ValidationError(
                {"danger_level": 'Красный уровень должен быть меньше чем желтый'}
            )
        if not 0 <= scoring_settings['warning_level'] <= 1:
            raise ValidationError(
                {"warning_level": 'Значение должно находиться в интервале [0, 1]'}
            )
        if not 0 <= scoring_settings['danger_level'] <= 1:
            raise ValidationError(
                {"danger_level": 'Значение должно находиться в интервале [0, 1]'}
            )
        return attrs

    class Meta:
        model = FinanceSettings
        fields = (
            'scoring',
            'currencies',
            'exchange_rates'
        )