# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from os import environ
from base64 import b64decode


SENDGRID_API_KEY = b64decode(environ.get("SENDGRID_TOKEN", ""))
environ['SENDGRID_API_KEY'] = SENDGRID_API_KEY