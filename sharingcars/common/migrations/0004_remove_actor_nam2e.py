# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-08 15:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_actor_nam2e'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actor',
            name='nam2e',
        ),
    ]
