# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-09-16 02:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_id', models.CharField(blank=True, max_length=12)),
                ('name', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant_id', models.CharField(blank=True, max_length=10)),
                ('name', models.CharField(blank=True, max_length=30)),
                ('date_admission', models.DateField()),
                ('created_by', models.CharField(blank=True, max_length=25)),
                ('updated_by', models.CharField(blank=True, max_length=25)),
                ('created_time', models.CharField(blank=True, max_length=50)),
                ('updated_time', models.CharField(blank=True, max_length=50)),
                ('active_status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Puskesmas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puskesmas_id', models.CharField(blank=True, max_length=5)),
                ('name', models.CharField(blank=True, max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='participant',
            name='puskesmas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Puskesmas'),
        ),
        migrations.AddField(
            model_name='child',
            name='mother',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Participant'),
        ),
    ]
