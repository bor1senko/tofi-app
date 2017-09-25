# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from finance.fixtures import init_deposit_templates, init_credit_templates
from django.core.management import BaseCommand


logger = logging.getLogger('jupiter')


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        logger.info('Initializing deposit templates...')
        init_deposit_templates()
        logger.info('Initializing deposit templates complete')
        logger.info('Initializing credits templates...')
        init_credit_templates()
        logger.info('Initializing credits templates complete')
