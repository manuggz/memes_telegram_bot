# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0013_auto_20150713_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensaje',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 13, 22, 23, 28, 260000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
