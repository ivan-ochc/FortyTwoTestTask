# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smartfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0006_auto_20151223_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=smartfields.fields.ImageField(blank=True, upload_to='img/'),
        ),
    ]
