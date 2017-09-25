# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.exceptions import FieldError
from rest_framework.filters import BaseFilterBackend


class GenericOrderingFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        param = request.query_params.get('ordering')
        if param:
            model_fields = {f.name for f in queryset.model._meta.get_fields()}
            ordering_fields = {f.strip() for f in param.split(',')}
            return queryset.order_by(*(model_fields and ordering_fields))
        return queryset


class GenericFieldFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        for param, value in request.query_params.iteritems():
            try:
                queryset = queryset.filter(**{param: value})
            except FieldError:
                continue
        return queryset
