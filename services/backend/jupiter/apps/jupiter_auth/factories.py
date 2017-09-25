# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import factory, random
from django.contrib.auth import get_user_model
from factory.fuzzy import FuzzyInteger
from faker import Faker
from jupiter_auth.models import UserProfile


fake = Faker()


class UserProfileFactory(factory.DjangoModelFactory):

    identification_number = factory.lazy_attribute(lambda obj: str(random.randrange(1000000, 9999999)) +
                                                   chr(ord('A')+random.randint(0, 25)) +
                                                   str(random.randrange(100, 999)) +
                                                   chr(ord('A')+random.randint(0, 25)) +
                                                   chr(ord('A')+random.randint(0, 25)) +
                                                   str(random.randrange(0, 9)))
    passport_number = factory.sequence(lambda obj:
                                       ['AB', 'BM', 'HB', 'KH', 'MP', 'MC', 'KB', 'PP'][random.randint(0, 7)] +
                                       str(random.randrange(1000000, 9999999)))
    phone = factory.sequence(lambda n: fake.phone_number())
    address = factory.sequence(lambda n: fake.address())
    age = FuzzyInteger(20, 70)
    passport_expires = factory.sequence(lambda n: fake.date())
    birth_date = factory.sequence(lambda n: fake.date())
    family_status = factory.sequence(lambda n: fake.sentence(nb_words=5))
    dependants = FuzzyInteger(0, 5)
    income = FuzzyInteger(100, 100000)
    realty = factory.sequence(lambda n: fake.sentence(nb_words=15))
    job = factory.sequence(lambda n: "{}, {}".format(fake.company(), fake.job()))
    user = factory.SubFactory('jupiter_auth.factories.UserFactory', profile=None)

    class Meta:
        model = UserProfile


class UserFactory(factory.DjangoModelFactory):

    username = factory.lazy_attribute(lambda obj: "{}-{}".format(obj.first_name, obj.last_name))
    email = factory.lazy_attribute(lambda obj: "{}@gmail.com".format(obj.username))
    first_name = factory.sequence(lambda n: fake.first_name())
    last_name = factory.sequence(lambda n: fake.last_name())
    profile = factory.RelatedFactory(UserProfileFactory, 'user')
    password = 'password'

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if extracted:
            self.groups.add(*extracted)

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if extracted:
            self.user_permissions.add(*extracted)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = get_user_model().objects.filter(username=kwargs.get('username')).first()
        if user:
            return user
        else:
            is_superuser = kwargs.get('is_superuser')
            if is_superuser:
                return get_user_model().objects.create_superuser(*args, **kwargs)
            else:
                return get_user_model().objects.create_user(*args, **kwargs)

    class Meta:
        model = get_user_model()
