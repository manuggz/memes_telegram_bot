# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0015_usuario_suscrito_actu'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoChat',
            fields=[
                ('id_chat', models.IntegerField(serialize=False, primary_key=True)),
                ('nombrechat', models.CharField(max_length=200, null=True)),
                ('suscrito_actu', models.BooleanField(default=True)),
            ],
        ),
    ]
