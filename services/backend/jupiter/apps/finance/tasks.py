# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from django_cron import CronJobBase, Schedule
from finance.models import Credit, Deposit, FinanceSettings


logger = logging.getLogger('jupiter')


def update_credits():
    objects = Credit.objects.exclude(status__in=Credit.INOPERABLE_STATUSES)
    for credit in objects:
        credit.daily_update()


def update_deposits():
    objects = Deposit.objects.exclude(status__in=Deposit.INOPERABLE_STATUSES)
    for deposit in objects:
        deposit.daily_update()


def daily_tasks():
    update_credits()
    update_deposits()


class DailyUpdate(CronJobBase):
    schedule = Schedule(run_every_mins=60 * 24)
    code = 'finance.tasks.DailyUpdate'

    def do(self):
        logger.info('Daily update of credits...')
        update_credits()
        logger.info('Daily update of credits complete')

        logger.info('Daily update of deposits...')
        update_deposits()
        logger.info('Daily update of deposits complete\n\n')


class SyncCurrencies(CronJobBase):
    schedule = Schedule(run_every_mins=60 * 12)
    code = 'finance.tasks.SyncCurrencies'

    def do(self):
        logger.info('Syncing currencies...')
        FinanceSettings.get_instance().update_exchange_rates()
        logger.info('Syncing currencies complete\n\n')
