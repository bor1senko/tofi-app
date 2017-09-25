# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.test import APITestCase

from core.api.generic.tests import ReadOnlyModelTestMixin
from finance.factories import DepositTemplateFactory, DepositFactory


class CreditTemplateTestCase(ReadOnlyModelTestMixin, APITestCase):

    check_view_perm = False
    base_name = 'deposit-templates'
    factory_class = DepositTemplateFactory


class CreditTestCase(ReadOnlyModelTestMixin, APITestCase):

    base_name = 'deposits'
    factory_class = DepositFactory