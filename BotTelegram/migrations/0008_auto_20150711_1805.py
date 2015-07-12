# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BotTelegram', '0007_auto_20150711_1757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mensaje',
            name='imagen_enviada',
        ),
    ]
