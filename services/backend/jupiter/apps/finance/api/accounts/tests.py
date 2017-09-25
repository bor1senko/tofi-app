# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.test import APITestCase

from core.api.generic.tests import ReadOnlyModelTestMixin
from finance.factories import AccountFactory


# class AccountTestCase(ReadOnlyModelTestMixin, APITestCase):
#
#     base_name = 'accounts'
#     factory_class = AccountFactory
