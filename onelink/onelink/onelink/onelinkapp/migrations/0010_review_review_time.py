# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-19 13:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('onelinkapp', '0009_auto_20170619_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
