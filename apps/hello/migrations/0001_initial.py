# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('username', models.CharField(unique=True, max_length=40)),
                ('first_name', models.CharField(max_length=40, blank=True)),
                ('last_name', models.CharField(max_length=40, blank=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('jabber', models.CharField(unique=True, max_length=40)),
                ('skype', models.CharField(unique=True, max_length=40)),
                ('is_admin', models.BooleanField(default=False)),
                ('bio', models.TextField()),
                ('other_contacts', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WebRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('host', models.CharField(max_length=1000)),
                ('path', models.CharField(max_length=1000)),
                ('method', models.CharField(max_length=50)),
                ('uri', models.CharField(max_length=2000)),
                ('status_code', models.IntegerField()),
                ('get', models.TextField(blank=True, null=True)),
                ('post', models.TextField(blank=True, null=True)),
                ('is_secure', models.BooleanField()),
                ('is_ajax', models.BooleanField()),
            ],
        ),
    ]
