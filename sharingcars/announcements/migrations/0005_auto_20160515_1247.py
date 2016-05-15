# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-15 10:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0004_auto_20160515_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyannouncement',
            name='announcement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='announcements.Announcement'),
        ),
        migrations.AlterField(
            model_name='applyannouncement',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.User'),
        ),
        migrations.AlterField(
            model_name='commentannouncement',
            name='announcement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='announcements.Announcement'),
        ),
        migrations.AlterField(
            model_name='commentannouncement',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.User'),
        ),
    ]