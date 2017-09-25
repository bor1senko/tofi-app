# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings


class CrossOriginResourceSharing(object):

    __allowed_origins = '*'
    __allowed_methods = ['PATCH', 'POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']

    allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', __allowed_origins)
    allowed_methods = getattr(settings, 'CORS_ALLOWED_METHODS', __allowed_methods)

    headers = getattr(settings, 'CORS_HEADERS', {
        'Access-Control-Allow-Origin': allowed_origins,
        'Access-Control-Allow-Methods': ",".join(allowed_methods),
    })

    def __init__(self, handler):
        self._get_response = handler

    def __call__(self, request):
        response = self._get_response(request)
        for k, v in self.headers.iteritems():
            response[k] = v
        return response
