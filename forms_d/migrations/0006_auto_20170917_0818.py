# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-09-17 01:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms_d', '0005_auto_20170917_0130'),
    ]

    operations = [
        migrations.AddField(
            model_name='d7infection',
            name='d7c_csf_microorganism_exist',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='d7infection2',
            name='d7c_csf_microorganism_exist',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='d7infection3',
            name='d7c_csf_microorganism_exist',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='d7infection4',
            name='d7c_csf_microorganism_exist',
            field=models.NullBooleanField(),
        ),
    ]
