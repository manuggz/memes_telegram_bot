# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0011_auto_20150713_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensaje',
            name='texto_enviado',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
