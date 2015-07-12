# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0009_auto_20150711_1808'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mensaje',
            name='imagen_enviadand',
        ),
        migrations.AddField(
            model_name='mensaje',
            name='enviado',
            field=models.ForeignKey(to='BotTelegram.NodoImagen', null=True),
        ),
    ]
