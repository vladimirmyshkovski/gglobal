# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-01 17:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_auto_20170617_0305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='slug',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
