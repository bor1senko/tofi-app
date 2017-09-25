# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


CLIENTS_GROUP = 'Clients'
ADMINS_GROUP = 'Admins'
GROUPS = [
    {
        "name": CLIENTS_GROUP,
        "permissions": [
            'manage_himself',
            'change_password_user',

            'view_credit',
            'leave_create_claim_credit',
            'open_online_credit',
            'make_payment_credit',
            'close_credit',

            'view_deposit',
            'leave_create_claim_deposit',
            'leave_close_claim_deposit',
            'put_money_deposit',

            'view_account',
            'leave_create_claim_account',
            'unassign_account',
            'assign_account',

            'view_contract',
            'view_transaction',
        ]
    },
    {
        "name": ADMINS_GROUP,
        "permissions": [
            'manage_himself',
            'view_user',
            'change_user',
            'change_password_user',

            'view_account',
            'confirm_create_claim_account',
            'reject_create_claim_account',

            'view_credit',
            'confirm_create_claim_credit',
            'reject_create_claim_credit',

            'view_deposit',
            'confirm_create_claim_deposit',
            'reject_create_claim_deposit',
            'confirm_close_claim_deposit',
            'reject_close_claim_deposit',

            'view_contract',
            'view_transaction',
            'view_financesettings',
            'change_financesettings'
        ]
    }
]


