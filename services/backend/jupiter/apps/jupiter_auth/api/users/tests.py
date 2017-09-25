# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from core.api.generic.tests import ReadOnlyModelTestMixin
from core.api.generic.utils import prettify_response
from jupiter_auth.factories import UserFactory


class UserTestCase(ReadOnlyModelTestMixin, APITestCase):

    base_name = 'users'
    factory_class = UserFactory

    check_view_perm = False

    def test_list_endpoint(self):
        url = reverse(self.base_name + self.list_suffix)
        self.client.force_authenticate(self.user)

        r = self.client.get(url)
        self.assertTrue(
            status.is_success(r.status_code),
            prettify_response('Request should be successful', r)
        )
        self.compare_objects(self.model_cls.objects.filter(is_superuser=False), r.data)

    def test_client_can_view_himself(self):
        url = reverse('users-detail', args=("me",))
        perm = Permission.objects.get(codename='manage_himself')
        self.check_permission(perm, url, 'get')
