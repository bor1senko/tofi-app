# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

import finance.api.transactions.serializers as serializers
import finance.models as fin_models
from core.api.generic.views import ModelViewSet, GenericViewSet
from jupiter_auth.authentication import TokenAuthentication
from jupiter_auth.utils import get_or_create_clients_group, get_or_create_admins_group


class TransactionView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = serializers.TransactionSerializer
    queryset = fin_models.Transaction.objects.all()
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        queryset = super(TransactionView, self).get_queryset()
        if self.request.user.is_superuser:
            return queryset
        if get_or_create_admins_group() in self.request.user.groups.all():
            return queryset
        elif get_or_create_clients_group() in self.request.user.groups.all():
            return queryset.filter(client=self.request.user)
        else:
            return queryset.none()