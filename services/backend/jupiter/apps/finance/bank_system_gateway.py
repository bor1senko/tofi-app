# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from Crypto.Cipher import AES
from Crypto.Hash import SHA512


def perform_bank_operation(request):
    """
        Send "OK" every time
    """
    AES_KEY = 'hLmclr[1C9ud4zrF'
    AES_IV = 16 * '\x10'
    AES_MODE = AES.MODE_CBC
    encryptor = AES.new(AES_KEY, AES_MODE, AES_IV)
    message = 'OK'.rjust(1024, '#') + SHA512.new('OK').hexdigest()
    ds = encryptor.encrypt(message)
    return ds
