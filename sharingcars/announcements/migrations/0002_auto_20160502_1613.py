# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-02 14:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        ('announcements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentannouncement',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='common.User'),
        ),
        migrations.AddField(
            model_name='applyannouncement',
            name='announcement',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='announcements.Announcement'),
        ),
        migrations.AddField(
            model_name='applyannouncement',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='common.User'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='common.User'),
        ),
    ]
