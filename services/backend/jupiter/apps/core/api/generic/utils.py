# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def prettify_response(message, response):
    msg = '{}.\nStatus code: {}\nData: {}'
    return msg.format(message,  response.status_code, response.data)
