# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0008_signalslog'),
    ]

    operations = [
        migrations.AddField(
            model_name='webrequest',
            name='priority',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
