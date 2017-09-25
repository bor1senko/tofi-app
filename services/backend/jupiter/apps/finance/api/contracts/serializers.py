# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.serializers import ModelSerializer
import finance.models as fin_models


class ContractSerializer(ModelSerializer):
    class Meta:
        model = fin_models.Contract
