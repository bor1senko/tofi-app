# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from djmoney.models.fields import MoneyField


def money_field(default=0, *args, **kwargs):
    return MoneyField(
        max_digits=15,
        decimal_places=2,
        default_currency='BYN',
        default=default,
        *args,
        **kwargs
    )


def percentage_field(*args, **kwargs):
    return models.DecimalField(
        max_digits=6,
        decimal_places=3,
        default=0,
        *args,
        **kwargs
    )
