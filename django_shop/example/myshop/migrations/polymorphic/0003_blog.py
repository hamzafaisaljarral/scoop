# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-18 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0002_auto_20180818_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Blogtitle', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
    ]
