# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0012_auto_20150713_1306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='id',
        ),
        migrations.AddField(
            model_name='usuario',
            name='id_u',
            field=models.IntegerField(default=0, serialize=False, primary_key=True),
            preserve_default=False,
        ),
    ]
