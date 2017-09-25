# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from copy import copy

from django.contrib.auth.models import Permission
from rest_framework.permissions import DjangoModelPermissions


class JupiterPermission(DjangoModelPermissions):

    perms_map = {
        'OPTIONS': [],
        'HEAD': [],
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    authenticated_users_only = True

    def get_required_permissions(self, method, model_cls):
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name
        }
        perms_map = copy(self.perms_map)
        if 'view_{}'.format(model_cls.__name__.lower()) in model_cls._meta.permissions:
            perms_map['GET'] = []
        return [perm % kwargs for perm in perms_map[method]]

    def has_permission(self, request, view):
        model_cls = view.queryset and view.queryset.model
        model_name = model_cls._meta.model_name
        app_label = model_cls._meta.app_label

        perm = "{}.{}_{}".format(app_label, view.action, model_name)
        if request.user.has_perm(perm):
            return True
        else:
            return super(JupiterPermission, self).has_permission(request, view)