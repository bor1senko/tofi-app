# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import Permission
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from core.api.generic.utils import prettify_response
from jupiter_auth.factories import UserFactory


fake = Faker()


class AuthClient(APIClient):

    sign_in_url = '/api/sign-in/'
    sign_out_url = '/api/sign-out/'
    sign_up_url = '/api/sign-up/'
    auth_url = '/api/users/'

    def sign_in(self, username, password="password"):
        data = {"username": username, "password": password}
        return self.post(self.sign_in_url, data, format='json')

    def sign_out(self, token):
        url = self.sign_out_url + '?token={}'.format(token)
        return self.get(url)

    def sign_up(self, data):
        return self.post(self.sign_up_url, data, format='json')

    def authenticate(self, token):
        url = self.auth_url + '?token={}'.format(token)
        return self.get(url)


class SignInTestCase(APITestCase):

    client_class = AuthClient

    @classmethod
    def setUpTestData(cls):
        view_perm = Permission.objects.get(codename='view_user')
        cls.user = UserFactory(permissions=[view_perm])
        cls.inactive_user = UserFactory(is_active=False, permissions=[view_perm])

    def test_successful_sign_in(self):
        r = self.client.sign_in(self.user.username)
        self.assertEqual(
            r.status_code,
            status.HTTP_200_OK,
            prettify_response('Sign in failed', r)
        )
        self.assertIn(
            'token',
            r.data,
            prettify_response('Token should be in the response', r)
        )

        token = r.data['token']
        r = self.client.authenticate(token)
        self.assertEqual(
            r.status_code,
            status.HTTP_200_OK,
            prettify_response('Authentication failed', r)
        )
        return token

    def test_sign_in_with_incorrect_credentials(self):
        r = self.client.sign_in('incorrect_username', 'incorrect_password')
        self.assertEqual(
            r.status_code,
            status.HTTP_400_BAD_REQUEST,
            prettify_response('Sign in should be failed', r)
        )

    def test_sign_in_by_inactive_user(self):
        r = self.client.sign_in(self.inactive_user.username)
        self.assertEqual(
            r.status_code,
            status.HTTP_400_BAD_REQUEST,
            prettify_response('Sign in should be failed', r)
        )


class SignOutTestCase(APITestCase):

    client_class = AuthClient

    @classmethod
    def setUpTestData(cls):
        view_perm = Permission.objects.get(codename='view_user')
        cls.user = UserFactory(permissions=[view_perm])

    def test_successful_sign_out(self):
        r = self.client.sign_in(self.user.username)
        self.assertEqual(
            r.status_code,
            status.HTTP_200_OK,
            prettify_response('Sign in failed', r)
        )

        token = r.data.get('token')
        r = self.client.sign_out(token)
        self.assertEqual(
            r.status_code,
            status.HTTP_204_NO_CONTENT,
            prettify_response('Sign out failed', r)
        )

        r = self.client.authenticate(token)
        self.assertEqual(
            r.status_code,
            status.HTTP_403_FORBIDDEN,
            prettify_response('Authentication should be failed', r)
        )

    def test_sign_out_with_incorrect_token(self):
        r = self.client.sign_out('incorrect_token')
        self.assertEqual(
            r.status_code,
            status.HTTP_403_FORBIDDEN,
            prettify_response('Sign out should be failed', r)
        )


class SignUpTestCase(APITestCase):

    client_class = AuthClient

    @classmethod
    def setUpTestData(cls):
        cls.data = {
            "username": fake.user_name(),
            "password": "password",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "profile": {
                "identification_number": "1111111A222BC3",
                "passport_number": "KH1111111",
                "passport_expires": "2018-12-10",
            }
        }

    def test_successful_sign_up(self):
        r = self.client.sign_up(self.data)
        self.assertEqual(
            r.status_code,
            status.HTTP_201_CREATED,
            prettify_response('Sign up failed', r)
        )

        r = self.client.sign_in(self.data['username'])
        self.assertEqual(
            r.status_code,
            status.HTTP_400_BAD_REQUEST,
            prettify_response('Sign in failed', r)
        )

    def test_sign_up_without_email(self):
        data = {}
        r = self.client.sign_up(data)
        self.assertEqual(
            r.status_code,
            status.HTTP_400_BAD_REQUEST,
            prettify_response('Sign up should be failed', r)
        )
