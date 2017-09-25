# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'jupiter',
        'USER': os.environ.get('DB_PASSWORD', 'jupiter'),
        'PASSWORD': os.environ.get('DB_USER', 'jupiter'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', 6000),
    }
}
