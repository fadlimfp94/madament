# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-09-04 04:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms_a', '0003_auto_20170902_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='a5prepregnancysmoking',
            name='a5f_father_smoking_status',
            field=models.CharField(blank=True, choices=[('', ''), ('1', 'Smoker'), ('2', 'Ex-smoker'), ('0', 'Never smoke')], default='', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='a5prepregnancysmoking',
            name='a5m_mother_smoking_status',
            field=models.CharField(blank=True, choices=[('', ''), ('1', 'Smoker'), ('2', 'Ex-smoker'), ('0', 'Never smoke')], default='', max_length=1, null=True),
        ),
    ]
