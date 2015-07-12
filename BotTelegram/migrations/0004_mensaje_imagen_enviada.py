# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0003_auto_20150711_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensaje',
            name='imagen_enviada',
            field=models.ForeignKey(to='BotTelegram.Imagen', null=True),
        ),
    ]
