# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-31 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0007_auto_20160829_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentroute',
            name='comment',
            field=models.TextField(max_length=395),
        ),
    ]
