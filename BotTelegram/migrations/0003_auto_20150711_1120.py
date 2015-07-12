# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0002_auto_20150710_2040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_lista', models.IntegerField()),
                ('url_imagen', models.CharField(max_length=100)),
                ('ruta_imagen', models.CharField(max_length=50)),
                ('siguiente', models.ForeignKey(to='BotTelegram.Imagen')),
            ],
        ),
        migrations.AlterField(
            model_name='mensaje',
            name='texto_enviado',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='apellido',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombreusuario',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
