# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
from django.conf.urls import url, include


def collect_applications():
    backend_path = os.environ.get('BACKEND_PATH', '/backend/')
    apps_path = os.path.join(backend_path, 'jupiter/apps')
    apps = []
    for filename in os.listdir(apps_path):
        if os.path.isdir(os.path.join(apps_path, filename)):
            apps.append('{}'.format(filename))
    return apps


def collect_urls():
    urls = []
    for app in collect_applications():
        try:
            urls.append(url(r'^', include('{}.api.urls'.format(app))))
        except ImportError:
            pass
    return urls


def to_bool(value):
    return not str(value).lower() in ['false', 'no', '0']