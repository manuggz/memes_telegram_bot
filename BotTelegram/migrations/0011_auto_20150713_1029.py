# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0010_auto_20150711_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='alt_mensaje',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='imagen',
            name='ruta_imagen',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='imagen',
            name='url_imagen',
            field=models.CharField(max_length=200, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='listaimagen',
            name='txt_buscado',
            field=models.CharField(max_length=200, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='apellido',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombreusuario',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
