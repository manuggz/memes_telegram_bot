# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0005_auto_20150711_1214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagen',
            name='id',
        ),
        migrations.AlterField(
            model_name='imagen',
            name='url_imagen',
            field=models.CharField(max_length=100, serialize=False, primary_key=True),
        ),
    ]
