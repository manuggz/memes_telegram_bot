# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-06 22:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0005_auto_20161106_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='title',
            field=models.CharField(blank=True, default=b'', max_length=200, null=True),
        ),
    ]