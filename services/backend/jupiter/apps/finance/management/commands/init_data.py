# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging, random, datetime, pytz
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import Group

from jupiter_auth.models import User, UserProfile
from jupiter_auth.factories import UserFactory
from django.core.management import BaseCommand
from rest_framework.authtoken.models import Token
from finance.tasks import daily_tasks
from finance.fixtures import init_deposit_templates, init_credit_templates
from jupiter_auth.utils import get_or_create_clients_group, get_or_create_admins_group, init_groups
from finance.models import (
    Credit,
    CreditTemplate,
    Deposit,
    DepositTemplate,
    Account,
    Transaction,
    FinanceSettings
)


logger = logging.getLogger('jupiter')


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        del_everything()
        init_groups()
        init_deposit_templates()
        init_credit_templates()
        create_admins(3)
        logger.info('Admins generated.')
        create_clients(10)
        logger.info('Clients generated.')
        create_accounts()
        logger.info('Clients accounts generated.')
        create_credits()
        logger.info('Clients credits generated.')
        create_deposits()
        logger.info('Clients deposits generated.')
        run_daily_updates(3)
        modify_credits()
        logger.info('Credits have been modified')
        modify_deposits()
        logger.info('Deposits have been modified')
        run_daily_updates()
        set_fake_dates()
        logger.info('Fake dates setted')

        logger.info('Result:')
        logger.info('Generated transactions: {}'.format(len(list(Transaction.objects.all()))))

        all = fined = active = closed = paid_off = 0
        for credit in Credit.objects.all():
            all += 1
            if credit.status == Credit.STATUS_CLOSED:
                closed += 1
            elif credit.status == Credit.STATUS_OPENED:
                active += 1
            elif credit.status == Credit.STATUS_FINED:
                fined += 1
            elif credit.status == Credit.STATUS_PAID_OFF:
                paid_off += 1

        logger.info('Generated credits: {}, active: {}, closed: {}, paid off: {}, fined: {}'.
                    format(all, closed, active, paid_off, fined))

        all = active = closed = 0
        for deposit in Deposit.objects.all():
            all += 1
            if deposit.status == Deposit.STATUS_CLOSED:
                closed += 1
            elif deposit.status == Deposit.STATUS_ACTIVE:
                active += 1

        logger.info('Generated deposits: {}, active: {}, closed: {}'.
                    format(all, closed, active))

        UserFactory(
            username='root',
            password='root',
            email='root@root.com',
            is_superuser=True
        )


def simple_event(probability):
    l, r = 0, 1e4
    cur = random.randint(l, r)
    if cur < int(r * probability / 100.0):
        return True
    else:
        return False


def random_element(array):
    if len(array) == 1:
        return array[0]
    return array[random.randint(0, len(array) - 1)]


def del_everything():
    User.objects.all().delete()
    Token.objects.all().delete()
    UserProfile.objects.all().delete()
    Credit.objects.all().delete()
    Account.objects.all().delete()
    Deposit.objects.all().delete()
    Transaction.objects.all().delete()
    Group.objects.all().delete()
    CreditTemplate.objects.all().delete()
    DepositTemplate.objects.all().delete()


def create_admins(count=3):
    for i in range(count):
        admin = UserFactory(username='admin{}'.format(i), password='admin{}'.format(i))
        Token.objects.create(user=admin)
        admin_group = get_or_create_admins_group()
        admin.groups.add(admin_group)
    admin = User.objects.get(username='admin0')
    admin.save()


def create_clients(count=10):
    for i in range(count):
        client = UserFactory(username='client{}'.format(i), password='client{}'.format(i))
        Token.objects.create(user=client)
        client_group = get_or_create_clients_group()
        client.groups.add(client_group)

        if simple_event(30):
            client.profile.number_of_times_90_more_days_late = random.randint(0, 5)

        if simple_event(50):
            client.profile.number_of_times_60_89_days_late = random.randint(0, 7)

        if simple_event(70):
            client.profile.number_of_times_30_59_days_late = random.randint(0, 9)

        client.profile.save()


def create_accounts():
    for client in User.objects.all():
        if get_or_create_clients_group() in client.groups.all():
            accounts_count = random.randint(5, 10)
            for i in range(accounts_count):
                is_heavy_account = simple_event(10)
                money_range = random.randint(3000, 10000) if is_heavy_account else \
                    random.randint(300, 3000)
                Account.create(True, client, money_range)


def create_credits():
    templates_ids = [t.id for t in CreditTemplate.objects.all()]
    min_amount = {
        "Европа": 1000,
        "Калисто": 1000,
        "Ио": 500,
        "Адреаста": 15000,
        "Ганимед": 20000,
        "Ганимед+": 20000,
    }
    max_amount = {
        "Европа": 15000,
        "Калисто": 5000,
        "Ио": 3000,
        "Адреаста": 30000,
        "Ганимед": 50000,
        "Ганимед+": 50000,
    }
    for client in User.objects.all():
        if get_or_create_clients_group() in client.groups.all():
            credits_count = random.randint(2, 8)
            for i in range(credits_count):
                template_id = random_element(templates_ids)
                template = CreditTemplate.objects.get(pk=template_id)
                amount = random.randint(min_amount[template.name], max_amount[template.name])
                accounts = list(Account.objects.filter(client=client))
                if len(accounts) == 0:
                    continue
                account = accounts[0]
                if amount < 10:
                    continue
                credit = Credit.create_claim(client,
                                             template,
                                             amount,
                                             template.max_duration,
                                             CreditTemplate.ENSURING_FINE,
                                             Credit.INTO_ACCOUNT,
                                             account.id)
                if simple_event(70):
                    credit.confirm()


def create_deposits():
    templates_ids = [t.id for t in DepositTemplate.objects.all()]
    for client in User.objects.all():
        if get_or_create_clients_group() in client.groups.all():
            deposits_count = random.randint(2, 6)
            for i in range(deposits_count):
                template_id = random_element(templates_ids)
                template = DepositTemplate.objects.get(pk=template_id)
                currencies = template.currency.keys()
                currency = random_element(currencies)
                term_percent = random_element(list(template.currency[currency]['percentage']))
                accounts = list(Account.objects.filter(client=client))
                if len(accounts) == 0:
                    continue
                account = accounts[0]
                account_max_amount = float(account.residue.amount) / \
                    FinanceSettings.get_instance().exchange_rates[currency]
                amount = min(random.randint(300, 20000), account_max_amount)
                deposit = Deposit.create(client,
                                         template,
                                         amount,
                                         term_percent['term'],
                                         term_percent['percentage'],
                                         currency,
                                         account.id)
                if not deposit is None and simple_event(70):
                    deposit.confirm()


def pay_for_credit(credit):
    client = credit.client
    accounts = Account.objects.filter(client=client)
    if len(accounts) == 0:
        return
    richest_account = accounts[0]
    for account in accounts:
        if richest_account.residue.amount < account.residue.amount:
            richest_account = account
    if richest_account.residue.amount == 0:
        return
    amount = random.randint(0, min(credit.residue.amount, int(richest_account.residue.amount/2)))
    richest_account.get_money(amount)
    credit.pay(amount)


def fined_credit(credit):
    days = random.randrange(10, 100)
    credit.next_payment_term += relativedelta(days=-days)
    credit.save()
    for _ in range(days):
        credit.daily_update()
    pay_for_credit(credit)


def paid_off_and_close(credit):
    for i in range(random.randint(3, 10)):
        pay_for_credit(credit)
    credit.daily_update()
    if credit.status != Credit.STATUS_PAID_OFF:
        credit.pay(credit.residue.amount)
    credit.close()


def modify_credits():
    for_pay = []
    for_fined = []
    for_paid_off_and_close = []

    for credit in Credit.objects.all():
        type = random.randint(0, 2)
        if type == 0:
            for_pay.append(credit)
        elif type == 1:
            for_fined.append(credit)
        elif type == 2:
            for_paid_off_and_close.append(credit)

    for credit in for_pay:
        pay_for_credit(credit)

    for credit in for_fined:
        fined_credit(credit)

    for credit in for_paid_off_and_close:
        paid_off_and_close(credit)


def close_deposit(deposit):
    client = deposit.client
    accounts = Account.objects.filter(client=client)
    if len(accounts) == 0:
        return
    poor_account = accounts[0]
    for account in accounts:
        if poor_account.residue.amount > account.residue.amount:
            poor_account = account
    money_in_byn = FinanceSettings.get_instance().exchange_rates[deposit.currency] * \
                   float(deposit.amount.amount)
    account.put_money(money_in_byn)
    deposit.status = deposit.STATUS_CLOSED
    deposit.save()
    Transaction.objects.create(client=client,
                               product=deposit,
                               info='Депозит закрыт. Деньги в размере {} BYN переведены на счет {}'.
                               format(money_in_byn, account.number),
                               type=Transaction.TYPE_DEPOSIT_CONFIRM_CLOSE)


def modify_deposits():
    for_close = []
    for deposit in Deposit.objects.all():
        will_closed = simple_event(50)
        if will_closed:
            for_close.append(deposit)
    for deposit in for_close:
        close_deposit(deposit)


def run_daily_updates(days=5):
    for i in range(days):
        daily_tasks()


def set_fake_dates():
    for t in Transaction.objects.all():
        start_date = datetime.datetime.today()+relativedelta(days=-150)
        end_date = datetime.datetime.today()+relativedelta(days=-10)
        when_happened = random_date(start_date, end_date)
        t.created_on = when_happened
        t.save()

    first_priority = ['Создан счет',
                      'Подана заявка на депозит.',
                      'Подана заявка на кредит.',
                      'Заявка на кредит одобрена.',
                      'Депозит открыт.']

    days_offset = 180
    for sub_string in first_priority:
        transactions = filter_by_substring(Transaction.objects.all(), sub_string)
        for t in transactions:
            start_date = datetime.datetime.today()+relativedelta(days=-days_offset)
            end_date = datetime.datetime.today()+relativedelta(days=-(days_offset-5))
            when_happened = random_date(start_date, end_date)
            t.created_on = when_happened
            t.save()
        days_offset -= 5

    last_priority = ['Депозит закрыт.',
                     'Кредит закрыт.']

    days_offset = 10
    for sub_string in last_priority:
        transactions = filter_by_substring(Transaction.objects.all(), sub_string)
        for t in transactions:
            start_date = datetime.datetime.today()+relativedelta(days=-days_offset)
            end_date = datetime.datetime.today()+relativedelta(days=-(days_offset-8))
            when_happened = random_date(start_date, end_date)
            t.created_on = when_happened
            t.save()


def filter_by_substring(queryset, substring):
    result = []
    for q in queryset:
        if substring in q.info:
            result.append(q)
    return result


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    result = start + datetime.timedelta(seconds=random_second)
    return result.replace(tzinfo=pytz.UTC)
