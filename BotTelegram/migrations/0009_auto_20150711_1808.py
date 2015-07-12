# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0008_auto_20150711_1805'),
    ]

    operations = [

        migrations.AddField(
            model_name='mensaje',
            name='imagen_enviadand',
            field=models.ForeignKey(to='BotTelegram.NodoImagen', null=True),
        ),
    ]
