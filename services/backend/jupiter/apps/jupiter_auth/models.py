# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
from os import environ
from urllib2 import Request, urlopen

from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
from finance.utils import money_field
from finance.models import Credit, FinanceSettings
from jupiter_auth.utils import get_or_create_admins_group


class User(AbstractUser):

    first_name = models.CharField(max_length=300, null=False, blank=False)
    email = models.EmailField(
        blank=False,
        null=False,
        unique=True,
    )

    def get_scoring(self):
        if self.is_superuser or get_or_create_admins_group() in self.groups.all():
            return False, 'Скоринг вычисляется только для клиентов'

        user_credits = Credit.objects.filter(client=self)

        if self.profile.dependants is None:
            return False, 'Для использования сервиса скоринга ' \
                          'нужно указать количество членов семьи'

        if self.profile.income is None:
            return False, 'Для использования сервиса скоринга ' \
                          'нужно указать месячный доход'

        if self.profile.age is None and self.profile.birth_date is None:
            return False, 'Для использования сервиса скоринга ' \
                          'нужно указать дату рождения'

        try:
            age = (date.today() - self.profile.birth_date).days / 365
        except Exception:
            age = self.profile.age

        scoring_data = {
            "age": age or 20,
            "credit_monthly_payments": [
                float(value) for value in
                user_credits.values_list('minimum_monthly_pay', flat=True)
                if value > 0
            ],
            "credits_residue": [
                float(value) for value in
                user_credits.values_list('residue', flat=True)
                if value > 0
            ],
            "credit_limits": [
                float(value) for value in
                user_credits.values_list('total_sum', flat=True)
                if value > 0
            ],
            "MonthlyIncome": float(self.profile.income.amount),
            "NumberOfDependents": self.profile.dependants,
            "NumberOfTime30-59DaysPastDueNotWorse": self.profile.number_of_times_30_59_days_late,
            "NumberOfTime60-89DaysPastDueNotWorse": self.profile.number_of_times_60_89_days_late,
            "NumberOfTimes90DaysLate": self.profile.number_of_times_90_more_days_late,
            "NumberRealEstateLoansOrLines": user_credits.count() * 0.2,
            "NumberOfOpenCreditLinesAndLoans": user_credits.count()
        }

        scoring_host = environ.get("SCORING_HOST", 'scoring')
        scoring_port = environ.get("SCORING_PORT", 'scoring')
        url = 'http://{}:{}/api/credits/scoring/'.format(scoring_host, scoring_port)
        try:
            headers = {"Content-Type": "application/json"}
            req = Request(url, data=json.dumps(scoring_data), headers=headers)
            data = json.loads(urlopen(req).read())
        except Exception:
            return False, 'Ошибка при обращении к сервису кредитного скоринга'

        s = FinanceSettings.get_instance().scoring
        danger_level = s.get('danger_level', 0.3)
        warning_level = s.get('warning_level', 0.5)

        if 0 <= data['scoring_result'] <= danger_level:
            data['level'] = 'danger'
        elif danger_level <= data['scoring_result'] <= warning_level:
            data['level'] = 'warning'
        else:
            data['level'] = 'success'
        return True, data

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        permissions = (
            ('view_user', 'Can view users'),
            ('manage_himself', 'Can manage himself'),
            ('change_password_user', 'Can change password')
        )


class UserProfile(models.Model):

    user = models.OneToOneField(User, related_name='profile')
    identification_number = models.CharField(max_length=30)
    passport_number = models.CharField(max_length=20)
    passport_expires = models.DateField(null=False)
    address = models.CharField(max_length=300, null=True)
    phone = models.CharField(max_length=200, null=True)
    age = models.IntegerField(null=True, default=30)
    birth_date = models.DateField(null=True)
    family_status = models.TextField(null=True)
    dependants = models.IntegerField(default=3)
    income = money_field(default=1000)
    realty = models.TextField(null=True)
    job = models.TextField(null=True)
    number_of_times_90_more_days_late = models.IntegerField(default=0)
    number_of_times_30_59_days_late = models.IntegerField(default=0)
    number_of_times_60_89_days_late = models.IntegerField(default=0)

    def treat_days_late(self, days_late):
        if 30 <= days_late < 60:
            self.number_of_times_30_59_days_late += 1
        elif 60 <= days_late < 90:
            self.number_of_times_60_89_days_late += 1
        elif 90 <= days_late:
            self.number_of_times_90_more_days_late += 1
        self.save()

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'
