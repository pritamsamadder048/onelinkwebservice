# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-19 10:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onelinkapp', '0004_itemrequest_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_star', models.IntegerField()),
                ('quality_star', models.IntegerField()),
                ('value_star', models.IntegerField()),
                ('title', models.TextField()),
                ('comment', models.TextField()),
                ('user_id', models.IntegerField()),
                ('user_name', models.CharField(max_length=500)),
                ('provider_id', models.IntegerField()),
                ('request_id', models.IntegerField(blank=True, null=True)),
                ('history_id', models.IntegerField(blank=True, null=True)),
                ('itemhistory_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewitemhistory', to='onelinkapp.ItemRequest')),
                ('itemrequest_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewitemrequest', to='onelinkapp.ItemRequest')),
                ('provider_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewproviderdetail', to='onelinkapp.UserDetail')),
                ('servicehistory_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewservicehistory', to='onelinkapp.ServiceRequest')),
                ('servicerequest_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewservicerequest', to='onelinkapp.ServiceRequest')),
                ('user_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewuserdetail', to='onelinkapp.UserDetail')),
            ],
        ),
        migrations.AddField(
            model_name='itemorderhistory',
            name='request_type',
            field=models.CharField(blank=True, default='PRODUCT', max_length=10, null=True),
        ),
    ]
