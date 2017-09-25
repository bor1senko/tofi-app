# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.test import APITestCase

from core.api.generic.tests import ReadOnlyModelTestMixin
from finance.factories import ContractFactory


class ContractTestCase(ReadOnlyModelTestMixin, APITestCase):

    base_name = 'contracts'
    factory_class = ContractFactory