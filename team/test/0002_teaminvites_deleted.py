# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-30 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teaminvites',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]