# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-09-02 04:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms_a', '0002_auto_20170901_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='a4father',
            name='a4f_employment_status',
            field=models.CharField(blank=True, choices=[('', ''), ('1', 'Employed'), ('2', 'Self-employed'), ('3', 'Unemployed')], default='', max_length=1),
        ),
    ]
