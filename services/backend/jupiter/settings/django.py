# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import sys

from jupiter.utils import collect_applications, to_bool


SECRET_KEY = 'fa55uiv$$izc6=0%eu)aixt!2h#!#mjskw4^k=@u5uvdai-u3f'
BASE_DIR = os.environ.get('BACKEND_PATH', '..')
WSGI_APPLICATION = 'jupiter.wsgi.application'
ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'jupiter.urls'

APPS_ROOT = 'jupiter/apps'
sys.path.insert(0, os.path.join(BASE_DIR, APPS_ROOT))

AUTH_USER_MODEL = 'jupiter_auth.User'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
DEBUG = to_bool(os.environ.get('DJANGO_DEBUG', 'True'))


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djmoney',
    'django_cron',
] + collect_applications()


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'jupiter.cors.CrossOriginResourceSharing',
]

CRON_CLASSES = [
    "finance.tasks.DailyUpdate",
    "finance.tasks.SyncCurrencies",
]


STATIC_ROOT = os.path.join(os.path.join(BASE_DIR, 'jupiter'), '.static')
STATIC_URL = '/static/'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
