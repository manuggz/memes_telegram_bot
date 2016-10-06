# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-05 20:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='respuestaservidor',
            old_name='usuario',
            new_name='usuario_t',
        ),
        migrations.AddField(
            model_name='usuario',
            name='ultima_respuesta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='BotTelegram.RespuestaServidor'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(default=b'NoName', max_length=200),
        ),
    ]
