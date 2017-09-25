# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.serializers import ModelSerializer
import finance.models as fin_models
from jupiter_auth.api.users.serializers import UserSerializer


class TransactionSerializer(ModelSerializer):

    client = UserSerializer()

    class Meta:
        model = fin_models.Transaction
