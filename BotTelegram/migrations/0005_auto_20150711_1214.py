# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0004_mensaje_imagen_enviada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='siguiente',
            field=models.ForeignKey(to='BotTelegram.Imagen', null=True),
        ),
    ]
