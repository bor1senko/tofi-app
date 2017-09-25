# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from .rest_framework import *
from .django import *
from .db import *
from .logging import *
from .mail import *

if 'test' in sys.argv:
    from .test_settings import *