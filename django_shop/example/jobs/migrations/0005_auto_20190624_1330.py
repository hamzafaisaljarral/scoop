# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-06-24 11:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_auto_20190307_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobs',
            name='date',
        ),
        migrations.AddField(
            model_name='jobs',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='enter the date when your project will end.', verbose_name='when will your event end'),
        ),
        migrations.AddField(
            model_name='jobs',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='enter the date of project.', verbose_name='enter the date when you want it  '),
        ),
    ]