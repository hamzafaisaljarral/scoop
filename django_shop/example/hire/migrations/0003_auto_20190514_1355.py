# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-05-14 11:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_auto_20190307_1423'),
        ('hire', '0002_auto_20190206_1102'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=120)),
                ('order_id', models.CharField(max_length=120)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('success', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('Hireplugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.ProfileJob')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AlterField(
            model_name='hire',
            name='is_accepted',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='hire',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
    ]
