# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-09-26 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms_b3', '0003_auto_20170926_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='b3laboratorytest',
            name='b3m_rubella',
            field=models.CharField(blank=True, choices=[('', ''), ('1', 'Ig G'), ('2', 'Ig M'), ('0', 'No')], default='', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='b3pollutanexposure',
            name='b5m_housing_type',
            field=models.CharField(blank=True, choices=[('', ''), ('1', 'Landed House'), ('2', 'Flat/Apartment')], default='', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='b3pollutanexposure',
            name='b5m_landed_house_type',
            field=models.CharField(blank=True, choices=[('', ''), ('1', 'One story building'), ('2', 'More than one story building')], default='', max_length=1, null=True),
        ),
    ]