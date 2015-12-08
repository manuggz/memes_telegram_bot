# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
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
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url_imagen', models.CharField(max_length=200)),
                ('ruta_imagen', models.CharField(max_length=200)),
                ('textobuscado', models.CharField(max_length=200)),
                ('id_lista', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaServidor',
            fields=[
                ('id_mensaje', models.IntegerField(serialize=False, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('imagen_enviada', models.ForeignKey(to='BotTelegram.Imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_u', models.IntegerField(serialize=False, primary_key=True)),
                ('nombreusuario', models.CharField(max_length=200, null=True)),
                ('nombre', models.CharField(max_length=200, null=True)),
                ('apellido', models.CharField(max_length=200, null=True)),
                ('suscrito_actu', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='respuestaservidor',
            name='usuario',
            field=models.ForeignKey(to='BotTelegram.Usuario'),
        ),
    ]
