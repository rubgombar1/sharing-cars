# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-23 19:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0003_auto_20160508_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyroute',
            name='state',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('approach', 'Approach'), ('rejected', 'Rejected')], default='waiting', max_length=64),
        ),
    ]
