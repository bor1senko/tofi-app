# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s (%(asctime)s, %(module)s): %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'jupiter': {
            'handlers': ['console'],
            'level': 'ERROR',
        }
    }
}
