# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-02-06 09:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('profile', '0003_auto_20190204_1403'),
        ('jobs', '0003_auto_20190204_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, default='', help_text='Enter project details or anything else you want freelancer to know.', verbose_name='message project detail to freelancer')),
                ('price', models.IntegerField(blank=True, default='', help_text='enter your hourly price in $', verbose_name='enter the price ')),
                ('contact_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='When this person completed the contact form.', verbose_name='contact date')),
                ('was_contacted', models.BooleanField(default=False, help_text='Check this if someone has already reached out to this person.', verbose_name='has been contacted?')),
                ('notes', models.TextField(blank=True, default='', help_text='Internal notes relating to contacting this person.', verbose_name='contact notes')),
                ('referer', models.CharField(blank=True, default='', help_text='This is the page the visitor was on before coming to the contact page.', max_length=2048, verbose_name='referring page')),
                ('hiredprofile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile.Profile')),
                ('jobhiredfor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.Jobs')),
                ('profileofjobpublisher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.ProfileJob')),
            ],
        ),
        migrations.CreateModel(
            name='HirePluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='hire_hirepluginmodel', serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(blank=True, help_text='Optional. Title of the widget.', max_length=64, verbose_name='title')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
