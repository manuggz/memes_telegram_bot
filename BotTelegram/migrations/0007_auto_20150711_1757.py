# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0006_auto_20150711_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListaImagen',
            fields=[
                ('txt_buscado', models.CharField(max_length=100, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='NodoImagen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_lista', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='imagen',
            name='id_lista',
        ),
        migrations.RemoveField(
            model_name='imagen',
            name='siguiente',
        ),
        migrations.AddField(
            model_name='imagen',
            name='alt_mensaje',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nodoimagen',
            name='mdimagen',
            field=models.ForeignKey(to='BotTelegram.Imagen'),
        ),
        migrations.AddField(
            model_name='nodoimagen',
            name='siguiente',
            field=models.ForeignKey(to='BotTelegram.NodoImagen', null=True),
        ),
        migrations.AddField(
            model_name='listaimagen',
            name='primero',
            field=models.ForeignKey(to='BotTelegram.NodoImagen'),
        ),
    ]
