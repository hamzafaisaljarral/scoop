# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-06-26 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_profilejob_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilejob',
            name='client_token',
            field=models.TextField(max_length=500, null='True', verbose_name='client token'),
        ),
    ]
