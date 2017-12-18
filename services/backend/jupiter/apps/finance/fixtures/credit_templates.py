# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from finance.models import CreditTemplate


CREDIT_TEMPLATES = [
    {
        "name": "По плечу",
        "type": CreditTemplate.TYPE_CONSUMER,
        "description": "Деньги всегда, когда нужно!",
        "annual_percentage_rate": 18,
        "max_amount": {
            "fixed": 3000,
            "annual_income_mul": 4.1,
            "percent_of_purchase": None,
        },
        "min_amount": {
            "fixed": 100,
            "annual_income_mul": 0.7,
            "percent_of_purchase": None,
        },
        "max_duration": 18,
        "fine_percentage": 0.6,
        "issue_online": False,
        "allowed_ensuring": [
            CreditTemplate.ENSURING_PLEDGE
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
        "name": "На счастливые моменты",
        "type": CreditTemplate.TYPE_CONSUMER,
        "description": "Потребительский кредит на небольшую сумму.",
        "annual_percentage_rate": 11,
        "max_amount": {
            "fixed": 1000,
            "annual_income_mul": None,
            "percent_of_purchase": None,
        },
        "min_amount": {
            "fixed": 100,
            "annual_income_mul": None,
            "percent_of_purchase": None,
        },
        "max_duration": 36,
        "fine_percentage": 0.5,
        "issue_online": False,
        "allowed_ensuring": [
            CreditTemplate.ENSURING_FINE
        ],
        "detailed_info": "Возраст Кредитополучателя на момент подачи документов не менее 18 лет, "
                         " на момент истечения срока предоставления кредита не более 70 лет. "
    },

    {
        "name": "Гарант",
        "type": CreditTemplate.TYPE_CONSUMER,
        "description": "Потребительский экспресс кредит. ",
        "annual_percentage_rate": 16,
        "max_amount": {
            "fixed": 30000,
            "annual_income_mul": None,
            "percent_of_purchase": None,
        },
        "min_amount": {
            "fixed": 1000,
            "annual_income_mul": None,
            "percent_of_purchase": None,
        },
        "max_duration": 36,
        "fine_percentage": 0.7,
        "issue_online": True,
        "allowed_ensuring": [
            CreditTemplate.ENSURING_FINE
        ],
        "detailed_info": "Процентная ставка фиксированная:"
                "- 16,8% годовых (при выдаче наличными);"
                "- 16% годовых (при выдаче безналичным путем)."
                "Вы гражданин РБ или гражданин, имеющий вид на жительство, постоянно проживающий на территории Республики Беларусь"
                "Ваш возраст - от 21 до 60 лет"
                "Ваш стаж на текущем месте работы от 3 месяцев"
                "У вас есть регулярный, официально подтвержденный доход на территории Беларуси"
    },

    {
        "name": "Экспресс-кредит",
        "type": CreditTemplate.TYPE_SELLER,
        "description": "Кредит на автомобиль.",
        "annual_percentage_rate": 26.9,
        "max_amount": {
            "fixed": 3000,
            "annual_income_mul": None,
            "percent_of_purchase": 90,
        },
        "min_amount": {
            "fixed": 50,
            "annual_income_mul": None,
            "percent_of_purchase": 40,
        },
        "max_duration": 36,
        "fine_percentage": 0.3,
        "issue_online": True,
        "allowed_ensuring": [
            CreditTemplate.ENSURING_PLEDGE,
            CreditTemplate.ENSURING_SURETY
        ],
        "detailed_info":
            "Дополнительные условия:"
            "Вы гражданин РБ или гражданин, имеющий вид на жительство, постоянно проживающий на территории Республики Беларусь "
                        "Ваш возраст - от 18 до 69 лет "
                        "Ваш стаж на текущем месте работы от 3 месяцев "
                        "У вас есть регулярный, официально подтвержденный доход на территории Беларуси"
                        "Наличие регистрации (прописки) на территории Республики Беларусь. "
                        "Цель: На приобретение товаров"
    },

    {
        "name": "Новенький",
        "type": CreditTemplate.TYPE_SELLER,
        "description": "Кредит на приобретение уже построенной недвижимости.",
        "annual_percentage_rate": 29.9,
        "max_amount": {
            "fixed": 15000,
            "annual_income_mul": None,
            "percent_of_purchase": None,
        },
        "min_amount": {
            "fixed": 100,
            "annual_income_mul": None,
            "percent_of_purchase":None,
        },
        "max_duration": 60,
        "fine_percentage": 0.25,
        "issue_online": False,
        "allowed_ensuring": [
            CreditTemplate.ENSURING_PLEDGE
        ],
        "detailed_info":"Дополнительные условия: "
                        "Вы гражданин РБ или гражданин, имеющий вид на жительство, постоянно проживающий на территории Республики Беларусь "
                        "Ваш возраст - от 21 до 62 лет"
                        "Ваш стаж на текущем месте работы от 3 месяцев "
                        "У вас есть регулярный, официально подтвержденный доход на территории Беларуси"
                        "Наличие регистрации (прописки) на территории Республики Беларусь. "
                        "Необходимые документы:"
                        "Паспорт или вид на жительство"
                        "Нужна справка о доходах, при сумме кредита от 5000.00"
                        "Документ воинского учета (для мужчин, не достигших возраста 27 лет)"
                        "Вы можете оформить кредит онлайн, после чего заявку рассмотрит администратор. "
    },


]
