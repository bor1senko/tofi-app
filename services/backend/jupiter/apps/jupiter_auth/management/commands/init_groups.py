# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from jupiter_auth.utils import init_groups
from django.core.management import BaseCommand


logger = logging.getLogger('jupiter')


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        logger.info('Initializing groups...')
        init_groups()
        logger.info('Initializing groups complete')
