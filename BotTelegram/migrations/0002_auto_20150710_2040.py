# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='update',
            name='mensaje',
        ),
        migrations.AddField(
            model_name='mensaje',
            name='update_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Update',
        ),
    ]
