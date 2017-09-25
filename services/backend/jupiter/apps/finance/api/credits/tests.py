# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.test import APITestCase

from core.api.generic.tests import ReadOnlyModelTestMixin
from finance.factories import CreditTemplateFactory, CreditFactory


class CreditTemplateTestCase(ReadOnlyModelTestMixin, APITestCase):

    check_view_perm = False
    base_name = 'credit-templates'
    factory_class = CreditTemplateFactory


class CreditTestCase(ReadOnlyModelTestMixin, APITestCase):

    base_name = 'credits'
    factory_class = CreditFactory