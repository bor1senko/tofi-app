# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from finance.fixtures.credit_templates import CREDIT_TEMPLATES
from finance.fixtures.deposit_templates import DEPOSIT_TEMPLATES
from finance.models import DepositTemplate, CreditTemplate


logger = logging.getLogger('jupiter')


def init_deposit_templates():
    DepositTemplate.objects.exclude(name__in=[d['name'] for d in DEPOSIT_TEMPLATES]).delete()
    for data in DEPOSIT_TEMPLATES:
        DepositTemplate.objects.update_or_create(name=data['name'], defaults=data)
        logger.info('Initialized deposit template "{}"'.format(data['name']))


def init_credit_templates():
    CreditTemplate.objects.exclude(name__in=[d['name'] for d in CREDIT_TEMPLATES]).delete()
    for data in CREDIT_TEMPLATES:
        CreditTemplate.objects.update_or_create(name=data['name'], defaults=data)
        logger.info('Initialized credit template "{}"'.format(data['name']))
