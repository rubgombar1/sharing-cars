# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-29 09:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0006_auto_20160623_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='visibility',
            field=models.BooleanField(default=True),
        ),
    ]