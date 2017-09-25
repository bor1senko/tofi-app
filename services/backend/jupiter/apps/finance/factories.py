# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import factory
from factory.fuzzy import FuzzyChoice, FuzzyFloat, FuzzyInteger
from faker import Faker
from django.utils.timezone import now
from finance.models import (
    Product,
    Transaction,
    Contract,
    Account,
    Deposit,
    DepositTemplate,
    Credit,
    CreditTemplate
)


fake = Faker()


class ProductFactory(factory.DjangoModelFactory):

    client = factory.SubFactory('jupiter_auth.factories.UserFactory')
    name = factory.sequence(lambda n: fake.sentence(nb_words=1))
    description = factory.sequence(lambda n: fake.sentence(nb_words=10))

    class Meta:
        model = Product


class TransactionFactory(factory.DjangoModelFactory):

    client = factory.SubFactory('jupiter_auth.factories.UserFactory')
    product = factory.SubFactory('finance.factories.ProductFactory')
    info = factory.sequence(lambda n: fake.sentence(nb_words=15))
    created_on = factory.LazyFunction(now)

    class Meta:
        model = Transaction


class ContractFactory(factory.DjangoModelFactory):

    client = factory.SubFactory('jupiter_auth.factories.UserFactory')
    product = factory.SubFactory('finance.factories.ProductFactory')
    signed_on = factory.LazyFunction(now)

    class Meta:
        model = Contract


class AccountFactory(factory.DjangoModelFactory):

    residue = factory.sequence(lambda n: fake.pyint())
    status = FuzzyChoice(dict(Account.STATUS_CHOICES))

    class Meta:
        model = Account


class DepositTemplateFactory(factory.DjangoModelFactory):

    name = factory.sequence(lambda n: fake.sentence(nb_words=1))
    description = factory.sequence(lambda n: fake.sentence(nb_words=15))
    currency = factory.lazy_attribute(lambda n: '{}')
    capitalization = FuzzyChoice(dict(DepositTemplate.CAPITALIZATION_CHOICES))
    closing = FuzzyChoice(dict(DepositTemplate.CLOSING_CHOICES))
    prolongation = factory.sequence(lambda n: fake.pybool())
    additional_contributions = factory.sequence(lambda n: fake.pybool())

    class Meta:
        model = DepositTemplate


class DepositFactory(ProductFactory):

    amount = factory.sequence(lambda n: fake.pyint())
    status = FuzzyChoice(dict(Deposit.STATUS_CHOICES))
    start_date = factory.sequence(lambda n: fake.date())
    capitalization = FuzzyChoice(dict(DepositTemplate.CAPITALIZATION_CHOICES))
    closing = FuzzyChoice(dict(DepositTemplate.CLOSING_CHOICES))
    template = factory.SubFactory('finance.factories.DepositTemplateFactory')

    class Meta:
        model = Deposit


class CreditTemplateFactory(factory.DjangoModelFactory):

    name = factory.sequence(lambda n: fake.sentence(nb_words=1))
    description = factory.sequence(lambda n: fake.sentence(nb_words=15))
    annual_percentage_rate = factory.fuzzy.FuzzyInteger(1, 100)
    max_amount = factory.sequence(lambda n: '{}')
    min_amount = factory.sequence(lambda n: '{}')
    max_duration = FuzzyInteger(3, 60)
    fine_percentage = FuzzyInteger(1, 100)
    issue_online = factory.sequence(lambda n: fake.pybool())
    allowed_ensuring = [FuzzyChoice(dict(CreditTemplate.ENSURING_CHOICES)).fuzz()]

    class Meta:
        model = CreditTemplate


class CreditFactory(ProductFactory):

    residue = FuzzyInteger(1000, 100000)
    current_penalty = FuzzyInteger(100, 1000)
    next_payment_term = factory.sequence(lambda n: fake.date())
    duration = factory.sequence(lambda n: fake.pyint())
    start_date = factory.sequence(lambda n: fake.date())
    status = FuzzyChoice(dict(Credit.STATUS_CHOICES))
    fine_percentage = FuzzyFloat(100)
    method_of_ensuring = FuzzyChoice(dict(CreditTemplate.ENSURING_CHOICES))
    money_destination = FuzzyChoice(dict(Credit.MONEY_DESTINATION))
    template = factory.SubFactory('finance.factories.CreditTemplateFactory')

    class Meta:
        model = Credit
