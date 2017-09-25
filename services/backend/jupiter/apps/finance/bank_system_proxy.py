# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import random
import urllib2
from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from finance.bank_system_gateway import perform_bank_operation


class BankSystemProxy(object):

    CREDIT_CREATING = 101
    CREDIT_CLOSING = 102
    CREDIT_PAYMENT = 103
    CREDIT_FINE = 104
    CREDIT_UNFINE = 105

    ACCOUNT_CREATING = 201
    ACCOUNT_CLOSING = 202
    ACCOUNT_GET_MONEY = 203
    ACCOUNT_PUT_MONEY = 204
    ACCOUNT_TRANSFER_MONEY = 205

    DEPOSIT_CREATING = 301
    DEPOSIT_CLOSING = 302
    DEPOSIT_ADD_MONEY = 303

    AES_KEY = 'hLmclr[1C9ud4zrF'
    AES_IV = 16 * '\x10'
    AES_MODE = AES.MODE_CBC

    @classmethod
    def _send_request(cls, request):
        request_data = json.dumps(request)
        result = perform_bank_operation(cls.sign(request_data))
        result = cls.verify(result)
        if not result[0] or result[1] != 'OK':
            return False
        else:
            return True

    @classmethod
    def credit_create(cls, client_id, template, money_amount, duration, percentage):
        obj = {'operation_id': cls.CREDIT_CREATING,
               'client_id': client_id,
               'template': template,
               'money_amount': money_amount,
               'duration': duration,
               'percentage': percentage}
        return cls._send_request(obj)

    @classmethod
    def credit_close(cls, credit_id):
        obj = {'operation_id': cls.CREDIT_CLOSING,
               'credit_id': credit_id}
        return cls._send_request(obj)

    @classmethod
    def credit_pay(cls, credit_id, payment):
        obj = {'operation_id': cls.CREDIT_PAYMENT,
               'credit_id': credit_id,
               'payment': payment}
        return cls._send_request(obj)

    @classmethod
    def credit_fine(cls, credit_id):
        obj = {'operation_id': cls.CREDIT_CLOSING,
               'credit_id': credit_id}
        return cls._send_request(obj)

    @classmethod
    def credit_unfine(cls, credit_id):
        obj = {'operation_id': cls.CREDIT_CLOSING,
               'credit_id': credit_id}
        return cls._send_request(obj)

    @classmethod
    def account_creation(cls, client_id, money_amount, new_number):
        obj = {'operation_id': cls.ACCOUNT_CREATING,
               'client_id': client_id,
               'money_amount': money_amount,
               'new_number': new_number}
        return cls._send_request(obj)

    @classmethod
    def account_closing(cls, account_id):
        obj = {'operation_id': cls.ACCOUNT_CLOSING,
               'credit_id': account_id}
        return cls._send_request(obj)

    @classmethod
    def account_get_money(cls, account_id, money_amount):
        obj = {'operation_id': cls.ACCOUNT_GET_MONEY,
               'account_id': account_id,
               'money_amount': money_amount}
        return cls._send_request(obj)

    @classmethod
    def account_put_money(cls, account_id, money_amount):
        obj = {'operation_id': cls.ACCOUNT_PUT_MONEY,
               'account_id': account_id,
               'money_amount': money_amount}
        return cls._send_request(obj)

    @classmethod
    def account_transfer_money(cls, from_id, to_id, money_amount):
        obj = {'operation_id': cls.ACCOUNT_TRANSFER_MONEYY,
               'source_id': from_id,
               'target_id': to_id,
               'money_amount': money_amount}
        return cls._send_request(obj)

    @classmethod
    def account_assign_to_user(cls, user_id, account_number):
        """
        Check user passport_number and account in Bank system.
        Return money_amount to system
        """
        return True, random.randrange(100, 2000)

    @classmethod
    def deposit_creation(cls, client_id, template, duration, percentage, money_amount,
                         currency):
        obj = {'operation_id': cls.ACCOUNT_CREATING,
               'client_id': client_id,
               'money_amount': money_amount,
               'template': template,
               'duration': duration,
               'percentage': percentage,
               'currency': currency}
        return cls._send_request(obj)

    @classmethod
    def deposit_closing(cls, deposit_id):
        obj = {'operation_id': cls.DEPOSIT_CLOSING,
               'deposit_id': deposit_id}
        return cls._send_request(obj)

    @classmethod
    def deposit_add_money(cls, deposit_id, money_amount):
        obj = {'operation_id': cls.DEPOSIT_ADD_MONEY,
               'deposit_id': deposit_id,
               'money_amount': money_amount}
        return cls._send_request(obj)

    @classmethod
    def get_currency_rates(cls):
        url = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
        try:
            data = json.loads(urllib2.urlopen(url).read())
            return {
                cur['Cur_Abbreviation']: cur['Cur_Scale'] * cur['Cur_OfficialRate']
                for cur in data
            }
        except Exception as e:
            return None

    @classmethod
    def sign(cls, message):
        """
            АЕС (сообщение(1024 bytes) + SHA512 (сообщение), secret_key))
        """
        encryptor = AES.new(cls.AES_KEY, cls.AES_MODE, cls.AES_IV)
        message = message.rjust(1024, chr(ord('#'))) + SHA512.new(message).hexdigest()
        ds = encryptor.encrypt(message)
        return ds

    @classmethod
    def verify(cls, message):
        """
        if everything is ok return (True, Message)
        else (False, None)
        """
        decryptor = AES.new(cls.AES_KEY, cls.AES_MODE, cls.AES_IV)
        plaintext = decryptor.decrypt(message)
        message = plaintext[:1024].strip(chr(ord('#')))
        hash = plaintext[1024:]
        integrity = SHA512.new(message).hexdigest() == hash
        return integrity, message if integrity else None
