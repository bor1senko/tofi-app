# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 23:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='status',
            field=models.IntegerField(choices=[(0, 'Opened'), (1, 'Fined'), (2, 'Paid off'), (3, 'Closed'), (4, 'Rejected'), (5, 'Requested')]),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='status',
            field=models.IntegerField(choices=[(0, 'Active'), (1, 'Closed'), (2, 'Rejected'), (3, 'Requested')]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.IntegerField(choices=[(101, ''), (102, ''), (103, ''), (104, ''), (105, ''), (106, ''), (107, ''), (108, ''), (201, ''), (202, ''), (203, ''), (204, ''), (205, ''), (206, ''), (207, ''), (208, ''), (209, ''), (210, ''), (301, ''), (302, ''), (303, ''), (304, ''), (305, ''), (306, ''), (307, ''), (308, ''), (309, ''), (310, ''), (666, '')], default=666),
        ),
    ]
