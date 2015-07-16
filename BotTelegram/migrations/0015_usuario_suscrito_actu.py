# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0014_mensaje_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='suscrito_actu',
            field=models.BooleanField(default=True),
        ),
    ]
