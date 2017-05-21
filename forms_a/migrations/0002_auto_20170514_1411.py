# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-14 07:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms_a', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='a2motheremployment',
            name='a2m_is_exposed_to_pollution',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='a2motheremployment',
            name='a2m_maternal_leave',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='a2motheremployment',
            name='a2m_travel_by_car',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='a2motheremployment',
            name='a2m_travel_by_cycling',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='a2motheremployment',
            name='a2m_travel_by_motorcycle',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='a2motheremployment',
            name='a2m_travel_by_public_transport',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='a2motheremployment',
            name='a2m_travel_by_walking',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='a2motheremployment',
            name='a2m_working_pregnancy',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_allergy_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_asthma_father',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_asthma_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_asthma_mother',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_asthma_sibling',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_cronic_cough_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_diabetes_complication',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_diabetes_father',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_diabetes_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_diabetes_mother',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_diabetes_sibling',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_eclampsia_complication',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_family_disease',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_heart_disease_coronary',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_heart_disease_father',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_heart_disease_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_heart_disease_mother',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_heart_disease_muscle',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_heart_disease_rhythm',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_heart_disease_sibling',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_heart_disease_valve',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_hypertension_complication',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_hypertension_father',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_hypertension_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_hypertension_mother',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_hypertension_sibling',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_infection_complication',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_is_use_insulin',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_medical_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_other_complication',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_other_disease',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_other_father',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_other_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_other_mother',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_other_sibling',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_preeclampsia_complication',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_previous_complication',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_previous_miscarriage',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_previous_premature',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_stroke_father',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_stroke_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_stroke_mother',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_stroke_sibling',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a3obstetric',
            name='a3m_tubercolosis_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_allergy_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_asthma_father',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_asthma_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_asthma_mother',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_asthma_sibling',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_cronic_cough_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_diabetes_father',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_diabetes_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_diabetes_mother',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_diabetes_sibling',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_family_disease',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_heart_disease_coronary',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_heart_disease_father',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_heart_disease_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_heart_disease_mother',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_heart_disease_muscle',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_heart_disease_rhythm',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_heart_disease_sibling',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_heart_disease_valve',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_hypertension_father',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_hypertension_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_hypertension_mother',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_hypertension_sibling',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_is_use_insulin',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_medical_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_other_disease',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_other_father',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_other_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_other_mother',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_other_sibling',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_stroke_father',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_stroke_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_stroke_mother',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_stroke_sibling',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a4father',
            name='a4f_tubercolosis_history',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a5prepregnancysmoking',
            name='a5f_father_smoke_pipes',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a5prepregnancysmoking',
            name='a5f_smoke_in_front_of_mother',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a5prepregnancysmoking',
            name='a5m_mother_smoke_pipes',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a5prepregnancysmoking',
            name='a5m_other_member_smoke',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='a5prepregnancysmoking',
            name='a5m_smoke_in_front_of',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='abaseline',
            name='is_save_all',
            field=models.NullBooleanField(default=False),
        ),
    ]