# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-02-04 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_auth', '0004_auto_20170411_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='freelancer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='jopublisher',
            field=models.BooleanField(default=False),
        ),
    ]
