# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-03 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jupiter_auth', '0012_auto_20161230_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='telegram',
            field=models.TextField(null=True),
        ),
    ]