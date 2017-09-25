# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from core.api.generic.permissions import JupiterPermission


class ManageSelfPermission(JupiterPermission):

    perm = 'jupiter_auth.manage_himself'

    def has_permission(self, request, view):
        username = view.kwargs.get('pk')
        if username == request.user.username or username == "me":
            if request.user.has_perm(self.perm):
                return True
        return super(ManageSelfPermission, self).has_permission(request, view)
