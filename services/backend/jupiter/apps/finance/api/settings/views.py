# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from core.api.generic.permissions import JupiterPermission
from finance.models import FinanceSettings
from finance.api.settings.serializers import FinanceSettingsSerializer
from jupiter_auth.authentication import TokenAuthentication


class FinanceSettingsView(RetrieveModelMixin,
                          UpdateModelMixin,
                          GenericViewSet):

    serializer_class = FinanceSettingsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (JupiterPermission,)
    queryset = FinanceSettings.objects.all()

    def get_object(self):
        return FinanceSettings.get_instance()