# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-06-26 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_auto_20190624_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilejob',
            name='customer_id',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]