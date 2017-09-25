# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from finance.models import DepositTemplate


DEPOSIT_TEMPLATES = [
    {
        "name": "Метида",
        "description": "Срочный отзывной банковский вклад",
        "currency": {
            "BYN": {
                "min_amount": 100,
                "max_term": 3,
                "percentage": [
                    {
                        "term": 3,
                        "percentage": 6
                    }
                ]
            },
            "USD": {
                "min_amount": 50,
                "max_term": 3,
                "percentage": [
                    {
                        "term": 3,
                        "percentage": 3.5,
                    }
                ]
            },
            "EUR": {
                "min_amount": 30,
                "max_term": 3,
                "percentage": [
                    {
                        "term": 3,
                        "percentage": 3.5,
                    }
                ]
            }
        },
        "capitalization": DepositTemplate.CAPITALIZATION_DAILY,
        "closing": DepositTemplate.CLOSING_ANYTIME,
        "prolongation": False,
        "additional_contributions": True,
        "detailed_info": "Срок вклада составляет 3 месяца. "
                         "Оформление происходит онлайн. "
                         "Вы указываете счет, с которого будут списаны средства. "
                         "После чего счет замораживается. "
                         "После подтверждения администратором со счета снимут указанную сумму, "
                         "а счет вновь станет активным. "
                         "Вклад предусматривает дополнительные взносы "
                         "Отозвать деньги вы можете в любой момент. "
                         "Для чего вы должны указать счет, на который "
                         "будут переведены деньги. Либо посетить отделение банка. "
    },

    {
        "name": "Карпо",
        "description": "Срочный безотзывный банковский вклад с "
                       "квартальной капитализацией и пролонгированияем.",
        "currency": {
            "BYN": {
                "min_amount": 200,
                "max_term": 36,
                "percentage": [
                    {
                        "term": 12,
                        "percentage": 6,
                    },
                    {
                        "term": 24,
                        "percentage": 8,
                    },
                    {
                        "term": 36,
                        "percentage": 10,
                    }
                ]
            },
            "USD": {
                "min_amount": 50,
                "max_term": 36,
                "percentage": [
                    {
                        "term": 12,
                        "percentage": 3
                    },
                    {
                        "term": 24,
                        "percentage": 3.5
                    },
                    {
                        "term": 36,
                        "percentage": 4
                    },
                ]
            },
            "EUR": {
                "min_amount": 70,
                "max_term": 36,
                "percentage": [
                    {
                        "term": 12,
                        "percentage": 3.5
                    },
                    {
                        "term": 24,
                        "percentage": 4
                    },
                    {
                        "term": 36,
                        "percentage": 4.5
                    },
                ]
            }
        },
        "capitalization": DepositTemplate.CAPITALIZATION_QUARTERLY,
        "closing": DepositTemplate.CLOSING_IN_END,
        "prolongation": True,
        "additional_contributions": False,
        "detailed_info": "Срок вклада составляет до 36 месяца. "
                         "Оформление происходит онлайн. "
                         "Вы указываете счет, с которого будут списаны средства. "
                         "После чего счет замораживается. "
                         "После подтверждения администратором со счета снимут указанную сумму, "
                         "а счет вновь станет активным. "
                         "Отозвать деньги вы можете только в конце срока вклада "
                         "(начиная за неделю до конца). "
                         "Если вы не закроете вклад после окончания срока (срок + неделя), "
                         "то вклад автоматически продлится на такой же срок. "
    },

    {
        "name": "Фива",
        "description": "Срочный безотзывной банковский "
                       "вклад с месячной капитализацией и без лонгирования.",
        "currency": {
            "BYN": {
                "min_amount": 100,
                "max_term": 32,
                "percentage": [
                    {
                        "term": 6,
                        "percentage": 5,
                    },
                    {
                        "term": 12,
                        "percentage": 6,
                    },
                    {
                        "term": 24,
                        "percentage": 7,
                    },
                    {
                        "term": 36,
                        "percentage": 8,
                    }
                ]
            },
            "USD": {
                "min_amount": 50,
                "max_term": 36,
                "percentage": [
                    {
                        "term": 6,
                        "percentage": 2
                    },
                    {
                        "term": 12,
                        "percentage": 2.5
                    },
                    {
                        "term": 24,
                        "percentage": 3
                    },
                    {
                        "term": 36,
                        "percentage": 3.5
                    },
                ]
            },
            "EUR": {
                "min_amount": 50,
                "max_term": 36,
                "percentage": [
                    {
                        "term": 6,
                        "percentage": 2,
                    },
                    {
                        "term": 12,
                        "percentage": 2.5,
                    },
                    {
                        "term": 24,
                        "percentage": 3,
                    },
                    {
                        "term": 36,
                        "percentage": 3.5,
                    },
                ]
            }
        },
        "capitalization": DepositTemplate.CAPITALIZATION_MONTHLY,
        "closing": DepositTemplate.CLOSING_IN_END,
        "prolongation": False,
        "additional_contributions": False,
        "detailed_info": "Срок вклада составляет до 36 месяца. "
                         "Оформление происходит онлайн. "
                         "Вы указываете счет, с которого будут списаны средства. "
                         "После чего счет замораживается. "
                         "После подтверждения администратором со счета снимут указанную сумму, "
                         "а счет вновь станет активным. "
                         "Отозвать деньги вы можете только в конце срока вклада "
                         "(начиная за неделю до конца). "
    },

    {
        "name": "Лида",
        "description": "Срочный безотзывный банковский вклад в белорусских рублях с лонгированием.",
        "currency": {
            "BYN": {
                "min_amount": 100,
                "max_term": 18,
                "percentage": [
                    {
                        "term": 6,
                        "percentage": 12,
                    },
                    {
                        "term": 12,
                        "percentage": 14,
                    },
                    {
                        "term": 18,
                        "percentage": 16,
                    }
                ]
            }
        },
        "capitalization": DepositTemplate.CAPITALIZATION_MONTHLY,
        "closing": DepositTemplate.CLOSING_IN_END,
        "prolongation": True,
        "additional_contributions": False,
        "detailed_info": "Отличные проценты для получения пассивной прибыли. "
                         "Срок вклада составляет до 18 месяцев.  "
                         "Оформление происходит онлайн. "
                         "Вы указываете счет, с которого будут списаны средства. "
                         "После чего счет замораживается. "
                         "После подтверждения администратором со счета снимут указанную сумму, "
                         "а счет вновь станет активным. "
                         "Отозвать деньги вы можете только в конце срока вклада "
                         "(начиная за неделю до конца), "
                         "Если вы не закроете вклад после окончания срока (срок + неделя), "
                         "то вклад автоматически продлится на такой же срок. "
    },

]
