# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
import datetime
from decimal import Decimal

from django.contrib.auth.models import Permission
from djmoney.models.fields import MoneyPatched
from rest_framework import status
from rest_framework.reverse import reverse

from core.api.generic.utils import prettify_response
from jupiter_auth.factories import UserFactory


class APITestMixin(object):

    base_name = None
    factory_class = None

    @classmethod
    def setUpClass(cls):
        cls.user = UserFactory(is_superuser=True)
        cls.object = cls.factory_class.create()
        cls.model_cls = cls.object.__class__

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.object.delete()

    def get_permission(self, prefix):
        app_label = self.model_cls._meta.app_label
        model_name = self.model_cls._meta.model_name
        codename = "{}_{}".format(prefix, model_name)
        return Permission.objects.get(content_type__app_label=app_label, codename=codename)

    def check_permission(self, perm, url, method):
        user = UserFactory()
        self.client.force_authenticate(user)
        r = getattr(self.client, method)(url)
        self.assertEqual(
            r.status_code, status.HTTP_403_FORBIDDEN,
            prettify_response('Request should be forbidden', r)
        )
        user.delete()

        user_with_perm = UserFactory(permissions=[perm])
        self.client.force_authenticate(user_with_perm)
        r = getattr(self.client, method)(url)
        self.assertTrue(
            status.is_success(r.status_code),
            prettify_response('Request should be successful', r)
        )
        user_with_perm.delete()

    def compare_field(self, field, obj_value, data_value):
        if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$', str(data_value)):
            data_value = datetime.datetime.strptime(str(data_value), '%Y-%m-%dT%H:%M:%S.%fZ')
            obj_value = datetime.datetime.strptime(
                str(obj_value)[:min(26, len(str(obj_value)))],
                '%Y-%m-%d %H:%M:%S.%f'
            )

        elif isinstance(obj_value, (int, long, float)):
            data_value = int(float(data_value))
            obj_value = int(float(obj_value))

        elif hasattr(obj_value, 'id'):
            obj_value = obj_value.id

        elif isinstance(obj_value, MoneyPatched):
            data_value = MoneyPatched(Decimal(data_value), currency='BYN')

        elif type(obj_value) != type(data_value):
            obj_value = str(obj_value)
            data_value = str(data_value)

        self.assertEqual(
            obj_value, data_value,
            '{} not equal (db: {}, r: {})'.format(field, obj_value, data_value)
        )

    def compare_object(self, obj, data):
        for field, data_value in data.iteritems():
            if hasattr(obj, field):
                obj_value = getattr(obj, field)
                if isinstance(data_value, dict):
                    self.compare_object(obj_value, data_value)
                elif isinstance(data_value, list) and hasattr(obj_value, 'all'):
                    self.compare_objects(obj_value.all(), data_value)
                else:
                    self.compare_field(field, obj_value, data_value)

    def compare_objects(self, objects, data_set):
        self.assertEqual(
            len(objects), len(data_set),
            "Objects count not equal(db: {}, r: {})".format(len(objects), len(data_set))
        )
        for obj, data in zip(objects, data_set):
            self.compare_object(obj, data)


class ListModelTestMixin(APITestMixin):

    list_suffix = '-list'
    check_view_perm = False

    def test_list_endpoint(self):
        url = reverse(self.base_name + self.list_suffix)
        self.client.force_authenticate(self.user)
        if self.check_view_perm:
            self.check_permission(self.get_permission('view'), url, 'get')

        r = self.client.get(url)
        self.assertTrue(
            status.is_success(r.status_code),
            prettify_response('Request should be successful', r)
        )
        self.compare_objects(self.model_cls.objects.all(), r.data)


class RetrieveModelTestMixin(APITestMixin):

    lookup_field = 'pk'
    detail_suffix = '-detail'
    check_view_perm = False

    def test_retrieve_endpoint(self):
        lookup = getattr(self.object, self.lookup_field)
        url = reverse(self.base_name + self.detail_suffix, args=(lookup,))
        self.client.force_authenticate(self.user)
        if self.check_view_perm:
            self.check_permission(self.get_permission('view'), url, 'get')

        r = self.client.get(url)
        self.assertTrue(
            status.is_success(r.status_code),
            prettify_response('Request should be successful', r)
        )
        self.compare_object(self.object, r.data)


class ReadOnlyModelTestMixin(ListModelTestMixin, RetrieveModelTestMixin, APITestMixin):
    pass
