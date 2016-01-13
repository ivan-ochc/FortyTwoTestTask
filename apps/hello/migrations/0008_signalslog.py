# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0007_auto_20151224_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignalsLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('type', models.CharField(max_length=7)),
                ('payload', models.CharField(max_length=1000)),
            ],
        ),
    ]
