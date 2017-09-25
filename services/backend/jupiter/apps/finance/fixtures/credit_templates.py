# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from finance.models import CreditTemplate


CREDIT_TEMPLATES = [
    {
        "name": "Европа",
        "type": CreditTemplate.TYPE_CONSUMER,
        "description": "Потребительский кредит на длительный срок.",
        "annual_percentage_rate": 29.2,
        "max_amount": {
            "fixed": 15000.0,
            "annual_income_mul": 4.1,
            "percent_of_purchase": None,
        },
        "min_amount": {
            "fixed": 1000.0,
            "annual_income_mul": 0.7,
            "percent_of_purchase": None,
        },
        "max_duration": 5*12,
        "fine_percentage": 0.6,
        "issue_online": False,
        "allowed_ensuring": [
            CreditTemplate.ENSURING_FINE
        ],
        "detailed_info": "Кредитный продукт, на базе которого вы выбираете "
                         "срок кредитования и сумму. Максимальная/минимальная суммы "
                         "кредита расчитывается на основании платежеспособности. "
                         "Выдается только в BYN. "
                         "Способ обеспечения - неустойка. "
                         "Неустойка начисляется за каждый день просрочки платежа, "
                         "как процент от остатка по кредиту + текущий штраф. "
                         "Вы можете оформить кредит онлайн, после чего заявку рассмотрит администратор. "
                         "Деньги могут быть переведены на указанный вами счет либо получены наличными, при этом "
                         "вы должны посетить банк, после подтверждения заявки администратором. "
    },

    {
        "name": "Калисто",
        "type": CreditTemplate.TYPE_CONSUMER,
        "description": "Потребительский кредит на небольшую сумму.",
        "annual_percentage_rate": 23.7,
        "max_amount": {
            "fixed": 5000,
            "annual_income_mul": None,
            "percent_of_purchase": None,
        },
        "min_amount": {
            "fixed": 1000,
            "annual_income_mul": None,
            "percent_of_purchase": None,
        },
        "max_duration": 18,
        "fine_percentage": 0.5,
        "issue_online": False,
        "allowed_ensuring": [
            CreditTemplate.ENSURING_FINE
        ],
        "detailed_info": "Очень удобен, если вам нужна небольшая сумма. "
                         "Процентная ставка вас приятно удивит. "
                         "Выдается на срок до 18 месяцев. "
                         "Выдается только в BYN. "
                         "Способ обеспечения - неустойка. "
                         "Неустойка начисляется за каждый день просрочки платежа, "
                         "как процент от остатка по кредиту + текущий штраф. "
                         "Вы можете оформить кредит онлайн, после чего заявку рассмотрит администратор. "
                         "Деньги могут быть переведены на указанный вами счет либо получены наличными, при этом "
                         "вы должны посетить банк, после подтверждения заявки администратором. "
    },

    {
        "name": "Ио",
        "type": CreditTemplate.TYPE_CONSUMER,
        "description": "Потребительский экспресс кредит. ",
        "annual_percentage_rate": 33,
        "max_amount": {
            "fixed": 3000,
            "annual_income_mul": None,
            "percent_of_purchase": None,
        },
        "min_amount": {
            "fixed": 500,
            "annual_income_mul": None,
            "percent_of_purchase": None,
        },
        "max_duration": 12,
        "fine_percentage": 0.7,
        "issue_online": True,
        "allowed_ensuring": [
            CreditTemplate.ENSURING_FINE
        ],
        "detailed_info": "Выдача производится онлайн. "
                         "Решение о выдаче кредита принимается системой кредитного скоринга. "
                         "Выдается только в BYN. Деньги переводятся на указанный вами расчетный счет. "
                         "Неустойка начисляется как процент от остатка по кредиту + текущий штраф. "
    },

    {
        "name": "Адреаста",
        "type": CreditTemplate.TYPE_SELLER,
        "description": "Кредит на автомобиль.",
        "annual_percentage_rate": 33,
        "max_amount": {
            "fixed": 100000,
            "annual_income_mul": None,
            "percent_of_purchase": 90,
        },
        "min_amount": {
            "fixed": 20000,
            "annual_income_mul": None,
            "percent_of_purchase": 40,
        },
        "max_duration": 7 * 12,
        "fine_percentage": 0.3,
        "issue_online": False,
        "allowed_ensuring": [
            CreditTemplate.ENSURING_PLEDGE,
            CreditTemplate.ENSURING_SURETY
        ],
        "detailed_info":"Максимальная и минимальная сумма кредиты определяются "
                        "на основании стоимости автомобиляю. "
                        "Автоматически переводит деньги "
                        "на счет продавца. Как способ обеспечения вы можете "
                        "выбрать либо залог автомобиля, либо поручительство. "
                        "В случае выбора поручительства, вам следует посетить банк на следующий календарный день "
                        "с данными о поручителе. "
                        "Выдается только в BYN. "
                        "Неустойка начисляется за каждый день просрочки платежа, как процент "
                        " от остатка по кредиту + текущий штраф. "
                        "Вы можете оформить кредит онлайн, после чего заявку рассмотрит администратор. "
    },

    {
        "name": "Ганимед",
        "type": CreditTemplate.TYPE_SELLER,
        "description": "Кредит на приобретение уже построенной недвижимости.",
        "annual_percentage_rate": 27,
        "max_amount": {
            "fixed": 200000,
            "annual_income_mul": None,
            "percent_of_purchase": 80,
        },
        "min_amount": {
            "fixed": 40000,
            "annual_income_mul": None,
            "percent_of_purchase": 50,
        },
        "max_duration": 10 * 12,
        "fine_percentage": 0.25,
        "issue_online": False,
        "allowed_ensuring": [
            CreditTemplate.ENSURING_PLEDGE
        ],
        "detailed_info":"Приобретаемая недвижимость является залогом. "
                        "Автоматически переводит деньги "
                        "на счет продавца. "
                        "Выдается только в BYN. "
                        "Неустойка начисляется за каждый день просрочки платежа, как процент "
                        " от остатка по кредиту + текущий штраф. "
                        "Вы можете оформить кредит онлайн, после чего заявку рассмотрит администратор. "
    },

    {
        "name": "Ганимед+",
        "type": CreditTemplate.TYPE_SELLER,
        "description": "Кредит на приобретение строящейся недвижимости.",
        "annual_percentage_rate": 27,
        "max_amount": {
            "fixed": 200000,
            "annual_income_mul": None,
            "percent_of_purchase": 90,
        },
        "min_amount": {
            "fixed": 40000,
            "annual_income_mul": None,
            "percent_of_purchase": 30,
        },
        "max_duration": 20 * 12,
        "fine_percentage": 0.2,
        "issue_online": False,
        "allowed_ensuring": [
            CreditTemplate.ENSURING_PLEDGE
        ],
        "detailed_info":"Приобретаемая недвижимость является залогом. "
                        "Автоматически переводит деньги "
                        "на счет продавца. "
                        "Выдается только в BYN. "
                        "Неустойка начисляется за каждый день просрочки платежа, как процент "
                        " от остатка по кредиту + текущий штраф. "
                        "Вы можете оформить кредит онлайн, после чего заявку рассмотрит администратор. "
    },

]
