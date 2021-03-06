# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-19 12:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onelinkapp', '0007_auto_20170619_1756'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='request_id',
            new_name='map_id',
        ),
        migrations.RemoveField(
            model_name='review',
            name='itemrequest_ref',
        ),
        migrations.RemoveField(
            model_name='review',
            name='servicerequest_ref',
        ),
        migrations.AddField(
            model_name='review',
            name='itemmapt_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewitemmap', to='onelinkapp.ItemMap'),
        ),
        migrations.AddField(
            model_name='review',
            name='servicemap_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewservicemap', to='onelinkapp.ServiceMap'),
        ),
    ]
