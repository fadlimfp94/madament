# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-15 18:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms_a', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='a1motherdemographic',
            name='a1m_education_level',
            field=models.CharField(choices=[('1', 'Illiterate'), ('2', 'Elementary'), ('3', 'High School'), ('4', 'Undergraduate'), ('5', 'Postgraduate')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='a1motherdemographic',
            name='a1m_marital_status',
            field=models.CharField(choices=[('1', 'Married'), ('2', 'Divorced/Unmaried')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='a1motherdemographic',
            name='a1m_residential_status',
            field=models.CharField(choices=[('1', 'Personal property'), ('2', 'Rent'), ('3', 'Family house')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='a2motheremployment',
            name='a2m_working_area',
            field=models.CharField(choices=[('1', 'Indoor'), ('2', 'Outdoor')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='a2motheremployment',
            name='a2m_working_status',
            field=models.CharField(choices=[('1', 'Employed'), ('2', 'Self-employed'), ('3', 'Unemployed')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_education_level',
            field=models.CharField(choices=[('1', 'Illiterate'), ('2', 'Elementary'), ('3', 'High School'), ('4', 'Undergraduate'), ('5', 'Postgraduate')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_employment_status',
            field=models.CharField(choices=[('1', 'Employed'), ('2', 'Unemployed'), ('3', 'Self-employed')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='a5prepregnancysmoking',
            name='a5c_colleagues_smoking_status',
            field=models.CharField(choices=[('1', 'Smoker'), ('2', 'Ex-smoker'), ('3', 'Never smoke')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='a5prepregnancysmoking',
            name='a5f_father_smoke_frequency',
            field=models.CharField(choices=[('1', 'Daily'), ('2', 'Weekly'), ('3', 'Monthly'), ('4', 'Never')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='a5prepregnancysmoking',
            name='a5f_father_smoking_status',
            field=models.CharField(choices=[('1', 'Smoker'), ('2', 'Ex-smoker'), ('3', 'Never smoke')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='a5prepregnancysmoking',
            name='a5m_mother_smoking_status',
            field=models.CharField(choices=[('1', 'Smoker'), ('2', 'Ex-smoker'), ('3', 'Never smoke')], default='', max_length=1),
        ),
    ]
