# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-29 11:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0007_announcement_visibility'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='departTime',
        ),
        migrations.AlterField(
            model_name='announcement',
            name='date',
            field=models.DateTimeField(),
        ),
    ]