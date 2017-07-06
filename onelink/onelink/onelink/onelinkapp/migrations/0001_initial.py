# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-15 13:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import onelinkapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('itemmap_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FavouriteService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('servicemap_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ItemMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviceprovider_id', models.IntegerField()),
                ('serviceprovider_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(max_length=20)),
                ('product_category_id', models.IntegerField()),
                ('item_name', models.CharField(max_length=500)),
                ('item_details', models.TextField()),
                ('item_features', models.TextField(blank=True, null=True)),
                ('item_image', models.TextField(blank=True, null=True)),
                ('item_MRP', models.FloatField()),
                ('item_SLP', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ItemNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviceprovider_id', models.IntegerField()),
                ('itemrequest_id', models.IntegerField()),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('request_type', models.CharField(blank=True, default='PRODUCT', max_length=10, null=True)),
                ('read', models.BooleanField(default=False)),
                ('notification', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemOrderHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviceprovider_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('item_map_id', models.IntegerField()),
                ('item_request_id', models.IntegerField()),
                ('confirmation_id', models.CharField(blank=True, max_length=500, null=True)),
                ('booked_time', models.DateTimeField(auto_now_add=True)),
                ('item_map_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iohservicemap', to='onelinkapp.ItemMap')),
            ],
        ),
        migrations.CreateModel(
            name='ItemRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviceprovider_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('item_category_id', models.IntegerField()),
                ('item_map_id', models.IntegerField()),
                ('item_quantity', models.IntegerField(default=1)),
                ('areapincode', models.CharField(blank=True, max_length=10, null=True)),
                ('item_request_address', models.TextField(blank=True, null=True)),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('request_detail', models.TextField(blank=True, null=True)),
                ('item_status', models.IntegerField(default=0)),
                ('item_map_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onelinkapp.ItemMap')),
            ],
        ),
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviceprovider_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('service_map_id', models.IntegerField()),
                ('service_request_id', models.IntegerField()),
                ('confirmation_id', models.CharField(blank=True, max_length=500, null=True)),
                ('booked_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=500)),
                ('product_detail', models.TextField()),
                ('product_image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=onelinkapp.models.product_image_upload_location, width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='RequestMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_id', models.IntegerField()),
                ('sender_id', models.IntegerField()),
                ('receiver_id', models.IntegerField()),
                ('sending_time', models.DateTimeField(auto_now_add=True)),
                ('message_text', models.TextField()),
                ('request_type', models.CharField(max_length=10)),
                ('read', models.BooleanField(default=False)),
                ('itemrequest_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='msgsservicerequest', to='onelinkapp.ItemRequest')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=500)),
                ('service_detail', models.TextField()),
                ('service_image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=onelinkapp.models.service_image_upload_location, width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviceprovider_id', models.IntegerField()),
                ('service_name', models.CharField(max_length=500)),
                ('license_no', models.CharField(max_length=40)),
                ('under_gov', models.CharField(max_length=40)),
                ('service_details', models.TextField()),
                ('serviceprovider_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(max_length=20)),
                ('service_category_id', models.IntegerField()),
                ('areapincode', models.CharField(max_length=10)),
                ('register_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('service_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onelinkapp.ServiceCategory')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviceprovider_id', models.IntegerField()),
                ('servicerequest_id', models.IntegerField()),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('request_type', models.CharField(blank=True, default='SERVICE', max_length=10, null=True)),
                ('read', models.BooleanField(default=False)),
                ('notification', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviceprovider_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('service_category_id', models.IntegerField()),
                ('service_map_id', models.IntegerField()),
                ('areapincode', models.CharField(max_length=10)),
                ('service_request_address', models.TextField(blank=True, null=True)),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('service_time', models.CharField(blank=True, max_length=200, null=True)),
                ('request_detail', models.TextField(blank=True, null=True)),
                ('service_status', models.IntegerField(default=0)),
                ('service_map_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onelinkapp.ServiceMap')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_service_name', models.CharField(max_length=500)),
                ('sub_service_detail', models.TextField()),
                ('service_categorgy_id', models.IntegerField()),
                ('service_categorgy_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onelinkapp.ServiceCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('open', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=500)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(max_length=20, unique=True)),
                ('pincode', models.CharField(max_length=10)),
                ('country', models.TextField()),
                ('city', models.TextField()),
                ('district', models.TextField()),
                ('building', models.TextField()),
                ('street', models.TextField()),
                ('key', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=200)),
                ('user_type', models.IntegerField(default=0)),
                ('user_createtime', models.DateTimeField(auto_now_add=True)),
                ('validemail', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('full_name', models.CharField(max_length=500)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(max_length=20, unique=True)),
                ('User_Type', models.IntegerField()),
                ('UserSession_starttime', models.DateTimeField(auto_now_add=True)),
                ('UserSession_lastmodifiedtime', models.DateTimeField(auto_now=True)),
                ('UserDetail_ref', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='onelinkapp.UserDetail')),
                ('UserDetail_id', models.IntegerField(unique=True)),
                ('UserSession_key', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserVerificationSession',
            fields=[
                ('full_name', models.CharField(max_length=500)),
                ('session_starttime', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(max_length=20, unique=True)),
                ('User_Type', models.IntegerField()),
                ('UserDetail_ref', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='onelinkapp.UserDetail')),
                ('UserDetail_id', models.IntegerField(unique=True)),
                ('UserSession_key', models.CharField(max_length=200, unique=True)),
                ('verificationtype', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='serviceprovider_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='providerdetail', to='onelinkapp.UserDetail'),
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='user_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userdetail', to='onelinkapp.UserDetail'),
        ),
        migrations.AddField(
            model_name='servicenotification',
            name='serviceprovider_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notiproviderdetail', to='onelinkapp.UserDetail'),
        ),
        migrations.AddField(
            model_name='servicenotification',
            name='servicerequest_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onelinkapp.ServiceRequest'),
        ),
        migrations.AddField(
            model_name='requestmessage',
            name='receiver_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msgreceiver', to='onelinkapp.UserDetail'),
        ),
        migrations.AddField(
            model_name='requestmessage',
            name='sender_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msgsender', to='onelinkapp.UserDetail'),
        ),
        migrations.AddField(
            model_name='requestmessage',
            name='servicerequest_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='msgsservicerequest', to='onelinkapp.ServiceRequest'),
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='service_map_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ohservicemap', to='onelinkapp.ServiceMap'),
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='service_request_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ohservicerequest', to='onelinkapp.ServiceRequest'),
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='serviceprovider_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ohproviderdetail', to='onelinkapp.UserDetail'),
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='user_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ohuserdetail', to='onelinkapp.UserDetail'),
        ),
        migrations.AddField(
            model_name='itemrequest',
            name='serviceprovider_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemproviderdetail', to='onelinkapp.UserDetail'),
        ),
        migrations.AddField(
            model_name='itemrequest',
            name='user_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemuserdetail', to='onelinkapp.UserDetail'),
        ),
        migrations.AddField(
            model_name='itemorderhistory',
            name='item_request_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iohsitemrequest', to='onelinkapp.ItemRequest'),
        ),
        migrations.AddField(
            model_name='itemorderhistory',
            name='serviceprovider_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iohproviderdetail', to='onelinkapp.UserDetail'),
        ),
        migrations.AddField(
            model_name='itemorderhistory',
            name='user_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iohuserdetail', to='onelinkapp.UserDetail'),
        ),
        migrations.AddField(
            model_name='itemnotification',
            name='itemrequest_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onelinkapp.ItemRequest'),
        ),
        migrations.AddField(
            model_name='itemnotification',
            name='serviceprovider_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inotiproviderdetail', to='onelinkapp.UserDetail'),
        ),
        migrations.AddField(
            model_name='itemmap',
            name='product_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onelinkapp.ProductCategory'),
        ),
        migrations.AddField(
            model_name='favouriteservice',
            name='servicemap_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onelinkapp.ServiceMap'),
        ),
        migrations.AddField(
            model_name='favouriteitem',
            name='itemmap_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onelinkapp.ItemMap'),
        ),
    ]