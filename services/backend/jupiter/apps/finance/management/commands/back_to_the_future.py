# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from datetime import datetime
from calendar import monthrange
from subprocess import call
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-d', '--delta', type=int)

    def handle(self, *args, **options):
        delta = options.get('delta', 2)
        today = datetime.now()
        for month in range(today.month, today.month + delta):
            min, max = monthrange(today.year, month)
            for day in range(1, max + 1):
                date = datetime(today.year, month, day)
                call(["date", datetime.strftime(date, '%m%d%Y')])
                call_command('runcrons', '--force', 'finance.tasks.DailyUpdate')
        call(["date", datetime.strftime(today, '%m%d%Y')])