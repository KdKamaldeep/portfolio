# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-07 13:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0004_auto_20161003_0752'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='hostedteamid',
            field=models.CharField(default='', max_length=200),
        ),
    ]