# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from core.api.generic.filters import GenericFieldFilter, GenericOrderingFilter
from core.api.generic.serializers import FieldInfoSerializer


class FieldsViewMixin(object):

    @list_route(methods=['get'])
    def fields(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if serializer_class:
            fields = serializer_class(context={'view': self}).get_fields()
            serializer = FieldInfoSerializer(fields.iteritems(), many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class OrderingViewMixin(object):

    def __init__(self, *args, **kwargs):
        super(OrderingViewMixin, self).__init__(*args, **kwargs)
        if self.queryset is not None:
            self.filter_backends = list(getattr(self, 'filter_backends', []))
            self.filter_backends += [GenericOrderingFilter]


class FilteringViewMixin(object):

    def __init__(self, *args, **kwargs):
        super(FilteringViewMixin, self).__init__(*args, **kwargs)
        if self.queryset is not None:
            self.filter_backends = list(getattr(self, 'filter_backends', []))
            self.filter_backends += [GenericFieldFilter]
