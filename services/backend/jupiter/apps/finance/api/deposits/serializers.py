# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.serializers import ModelSerializer
import finance.models as fin_models
from jupiter_auth.api.users.serializers import UserSerializer


class DepositTemplateSerializer(ModelSerializer):
    class Meta:
        model = fin_models.DepositTemplate


class DepositSerializer(ModelSerializer):

    client = UserSerializer()
    template = DepositTemplateSerializer()

    class Meta:
        model = fin_models.Deposit
