# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from jupiter_auth.settings import GROUPS, CLIENTS_GROUP, ADMINS_GROUP

from django.contrib.auth.models import Group, Permission


logger = logging.getLogger('jupiter')


def init_groups():
    Group.objects.exclude(name__in=[g['name'] for g in GROUPS]).delete()
    for group_data in GROUPS:
        perms = Permission.objects.filter(codename__in=group_data['permissions'])
        group, created = Group.objects.get_or_create(name=group_data['name'])
        group.permissions.clear()
        group.permissions.add(*perms)
        logger.info('Initialized group "{}"'.format(group_data['name']))


def get_or_create_clients_group():
    if not Group.objects.filter(name=CLIENTS_GROUP).exists():
        init_groups()
    return Group.objects.get(name=CLIENTS_GROUP)


def get_or_create_admins_group():
    if not Group.objects.filter(name=ADMINS_GROUP).exists():
        init_groups()
    return Group.objects.get(name=ADMINS_GROUP)
