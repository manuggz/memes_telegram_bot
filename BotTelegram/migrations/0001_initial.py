# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id_mensaje', models.IntegerField(serialize=False, primary_key=True)),
                ('texto_enviado', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('update_id', models.IntegerField(serialize=False, primary_key=True)),
                ('mensaje', models.ForeignKey(to='BotTelegram.Mensaje')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreusuario', models.CharField(max_length=200, null=True)),
                ('nombre', models.CharField(max_length=200)),
                ('apellido', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='mensaje',
            name='usuario',
            field=models.ForeignKey(to='BotTelegram.Usuario'),
        ),
    ]
