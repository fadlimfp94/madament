"""
CATATAN
=======
empty value pada model ini
 > Char = empty string
 > Boolean = false
 > Integer = None (Null)

semua IntergerField di sini memiliki sifat Null = True
"""

from __future__ import unicode_literals
from django.db import models
from core.models import *

class ABaseLine(models.Model):
	participant = models.ForeignKey(Participant, on_delete=models.PROTECT)
	interviewer_id = models.CharField(max_length=25)
	data_entry_id = models.CharField(max_length=25)
	data_checked_id = models.CharField(max_length=25, null=True)
	date_admission = models.DateField()
	date_interviewed = models.DateField()
	date_data_entered = models.DateField()
	date_data_checked = models.DateField(null=True)
	is_save_all = models.BooleanField(default=False)

class A1MotherDemographic(models.Model):
	a_form = models.ForeignKey(ABaseLine, on_delete=models.PROTECT)
	a1m_name = models.CharField(max_length=25)
	a1m_pob = models.CharField(max_length=25)
	a1m_dob = models.DateField()
	a1m_residence_street = models.CharField(max_length=25)
	a1m_residence_rt = models.CharField(max_length=3)
	a1m_residence_rw = models.CharField(max_length=3)
	a1m_residence_district = models.CharField(max_length=25)
	a1m_residence_city = models.CharField(max_length=25)
	a1m_residence_zipcode = models.CharField(max_length=10)
	a1m_moving_date = models.DateField()
	a1m_residing_duration = models.IntegerField(null=True)
	RESIDENTIAL_STATUS_LIST = (
						('1', 'Personal property'),
						('2', 'Rent'),
						('3', 'Family house'),	
		)
	a1m_residential_status = models.CharField(choices=RESIDENTIAL_STATUS_LIST, max_length=1, default="")
	###
	a1m_previous_residence_1st_start_year = models.IntegerField(null=True)
	a1m_previous_residence_1st_end_year = models.IntegerField(null=True)
	a1m_previous_residence_1st_district = models.CharField(max_length=25)
	a1m_previous_residence_1st_city = models.CharField(max_length=25)
	a1m_previous_residence_1st_zipcode = models.CharField(max_length=10)
	###
	a1m_previous_residence_2nd_start_year = models.IntegerField(null=True)
	a1m_previous_residence_2nd_end_year = models.IntegerField(null=True)
	a1m_previous_residence_2nd_district = models.CharField(max_length=25)
	a1m_previous_residence_2nd_city = models.CharField(max_length=25)
	a1m_previous_residence_2nd_zipcode = models.CharField(max_length=10)
	##
	a1m_previous_residence_3rd_start_year = models.IntegerField(null=True)
	a1m_previous_residence_3rd_end_year = models.IntegerField(null=True)
	a1m_previous_residence_3rd_district = models.CharField(max_length=25)
	a1m_previous_residence_3rd_city = models.CharField(max_length=25)
	a1m_previous_residence_3rd_zipcode = models.CharField(max_length=10)
	##
	a1m_previous_residence_4th_start_year = models.IntegerField(null=True)
	a1m_previous_residence_4th_end_year = models.IntegerField(null=True)
	a1m_previous_residence_4th_district = models.CharField(max_length=25)
	a1m_previous_residence_4th_city = models.CharField(max_length=25)
	a1m_previous_residence_4th_zipcode = models.CharField(max_length=10)
	##
	a1m_previous_residence_5th_start_year = models.IntegerField(null=True)
	a1m_previous_residence_5th_end_year = models.IntegerField(null=True)
	a1m_previous_residence_5th_district = models.CharField(max_length=25)
	a1m_previous_residence_5th_city = models.CharField(max_length=25)
	a1m_previous_residence_5th_zipcode = models.CharField(max_length=10)
	##
	a1m_home_phone_number = models.CharField(max_length=25)
	a1m_mobile_phone_number = models.CharField(max_length=25)
	a1m_email = models.EmailField()
	EDUCATION_LEVEL_LIST = (
						('1', 'Illiterate'),
						('2', 'Elementary'),
						('3', 'High School'),
						('4', 'Undergraduate'),
						('5', 'Postgraduate'),	
		)
	a1m_education_level = models.CharField(choices=EDUCATION_LEVEL_LIST, max_length=1, default="")
	a1m_family_income = models.IntegerField(null=True)
	MARITAL_STATUS_LIST = (
						('1', 'Married'),
						('2', 'Divorced/Unmaried'),	
		)
	a1m_marital_status = models.CharField(choices=MARITAL_STATUS_LIST,max_length=1, default="")
	##
	a1m_relative_name = models.CharField(max_length=25)
	a1m_relative_street = models.CharField(max_length=25)
	a1m_relative_rt = models.CharField(max_length=2)
	a1m_relative_rw = models.CharField(max_length=2)
	a1m_relative_district = models.CharField(max_length=25)
	a1m_relative_city = models.CharField(max_length=25)
	a1m_relative_zipcode = models.CharField(max_length=10)
	a1m_relative_home_phone_number = models.CharField(max_length=25)
	a1m_relative_mobile_phone_number = models.CharField(max_length=25)


class A2MotherEmployment(models.Model):
	a_form = models.ForeignKey(ABaseLine, on_delete=models.PROTECT)
	EMPLOYMENT_STATUS_LIST = (
						('1', 'Employed'),
						('2', 'Self-employed'),
						('3', 'Unemployed'),	
		)
	a2m_working_status = models.CharField(choices=EMPLOYMENT_STATUS_LIST, max_length=1, default="")
	a2m_working_type = models.CharField(max_length=25)
	a2m_working_pregnancy = models.BooleanField(default=False)
	a2m_maternal_leave = models.BooleanField(default=False)
	a2m_maternal_leave_duration = models.IntegerField(null=True)
	a2m_work_street = models.CharField(max_length=25)
	a2m_work_rt = models.CharField(max_length=3)
	a2m_work_rw = models.CharField(max_length=3)
	a2m_work_district = models.CharField(max_length=25)
	a2m_work_city = models.CharField(max_length=25)
	a2m_work_zipcode = models.CharField(max_length=10)
	a2m_work_phone_number = models.CharField(max_length=25)
	a2m_travel_by_car = models.BooleanField(default=False)
	a2m_travel_by_motorcycle = models.BooleanField(default=False)
	a2m_travel_by_public_transport = models.BooleanField(default=False)
	a2m_public_transport_type = models.CharField(max_length=25)
	a2m_travel_by_cycling = models.BooleanField(default=False)
	a2m_travel_by_walking = models.BooleanField(default=False)
	a2m_work_time_travel = models.IntegerField(null=True)
	a2m_is_exposed_to_pollution = models.BooleanField(default=False)
	a2m_working_hours = models.IntegerField(null=True)
	WORKING_AREA_LIST = (
						('1', 'Indoor'),
						('2', 'Outdoor'),	
		)
	a2m_working_area = models.CharField(choices=WORKING_AREA_LIST, max_length=1, default="")

## A3 sampao A5 belum diperbaiki nama fieldnya ##
class A3Obstetric(models.Model):
	a_form = models.ForeignKey(ABaseLine, on_delete=models.PROTECT)
	a3m_pre_pregnancy_weight = models.IntegerField(null=True)
	a3m_pre_pregnancy_height = models.IntegerField(null=True)
	a3m_first_day_last_menstruation = models.DateField()
	a3m_estimated_due_date = models.DateField()
	a3m_gravida = models.IntegerField(null=True)
	a3m_parity = models.IntegerField(null=True)
	a3m_abortus = models.IntegerField(null=True)
	a3m_previous_premature = models.BooleanField()
	a3m_previous_miscarriage = models.BooleanField()
	a3m_previous_complication = models.BooleanField()
	a3m_hypertension_complication = models.BooleanField()
	a3m_diabetes_complication = models.BooleanField()
	a3m_preeclampsia_complication = models.BooleanField()
	a3m_eclampsia_complication = models.BooleanField()
	a3m_infection_complication = models.BooleanField()
	a3m_other_complication = models.BooleanField()
	a3m_other_complication_name = models.CharField(max_length=25)
	a3m_medical_history = models.BooleanField()
	a3m_asthma_history = models.BooleanField()
	a3m_tubercolosis_history = models.BooleanField()
	a3m_cronic_cough_history = models.BooleanField()
	a3m_hypertension_history = models.BooleanField()
	a3m_heart_disease_history = models.BooleanField()
	a3m_heart_disease_coronary = models.BooleanField()
	a3m_heart_disease_valve = models.BooleanField()
	a3m_heart_disease_rhythm = models.BooleanField()
	a3m_heart_disease_muscle = models.BooleanField()
	a3m_diabetes_history = models.BooleanField()
	a3m_is_use_insulin = models.BooleanField()
	a3m_stroke_history = models.BooleanField()
	a3m_allergy_history = models.BooleanField()
	a3m_allergy_detail = models.CharField(max_length=25)
	a3m_other_history = models.BooleanField()
	a3m_other_detail = models.CharField(max_length=25)
	a3m_family_disease = models.BooleanField()
	a3m_asthma_mother = models.BooleanField()
	a3m_asthma_father = models.BooleanField()
	a3m_asthma_sibling = models.BooleanField()
	a3m_hypertension_mother = models.BooleanField()
	a3m_hypertension_father = models.BooleanField()
	a3m_hypertension_sibling = models.BooleanField()
	a3m_heart_disease_mother = models.BooleanField()
	a3m_heart_disease_father = models.BooleanField()
	a3m_heart_disease_sibling = models.BooleanField()
	a3m_diabetes_mother = models.BooleanField()
	a3m_diabetes_father = models.BooleanField()
	a3m_diabetes_sibling = models.BooleanField()
	a3m_stroke_mother = models.BooleanField()
	a3m_stroke_father = models.BooleanField()
	a3m_stroke_sibling = models.BooleanField()
	a3m_other_disease = models.BooleanField()
	a3m_other_disease_name = models.CharField(max_length=25)
	a3m_other_mother = models.BooleanField()
	a3m_other_father = models.BooleanField()
	a3m_other_sibling = models.BooleanField()

class A4Father(models.Model):
	a_form = models.ForeignKey(ABaseLine, on_delete=models.PROTECT)
	a4f_name = models.CharField(max_length=25)
	a4f_pob = models.CharField(max_length=25)
	a4f_dob = models.DateField()
	a4f_residence_street = models.CharField(max_length=25)
	a4f_residence_rt = models.CharField(max_length=3)
	a4f_residence_rw = models.CharField(max_length=3)
	a4f_residence_district = models.CharField(max_length=25)
	a4f_residence_city = models.CharField(max_length=25)
	a4f_residence_zipcode = models.CharField(max_length=10)
	a4f_home_phone_number = models.CharField(max_length=25)
	a4f_mobile_phone_number = models.CharField(max_length=25)
	a4f_email = models.EmailField()
	EDUCATION_LEVEL_LIST = (
						('1', 'Illiterate'),
						('2', 'Elementary'),
						('3', 'High School'),
						('4', 'Undergraduate'),
						('5', 'Postgraduate'),	
		)
	a4f_education_level = models.CharField(choices=EDUCATION_LEVEL_LIST, max_length=1, default="")
	a4f_weight = models.IntegerField(null=True)
	a4f_height = models.IntegerField(null=True)
	EMPLOYMENT_STATUS_LIST = (
						('1', 'Employed'),
						('2', 'Unemployed'),
						('3', 'Self-employed'),	
		)
	a4f_employment_status = models.CharField(choices=EMPLOYMENT_STATUS_LIST, max_length=1, default="")
	a4f_type_of_job = models.CharField(max_length=25)
	a4f_work_street = models.CharField(max_length=25)
	a4f_work_rt = models.CharField(max_length=3)
	a4f_work_rw = models.CharField(max_length=3)
	a4f_work_district = models.CharField(max_length=25)
	a4f_work_city = models.CharField(max_length=25)
	a4f_work_zipcode = models.CharField(max_length=10)
	a4f_work_phone_number = models.CharField(max_length=25)
	a4f_medical_history = models.BooleanField()
	a4f_asthma_history = models.BooleanField()
	a4f_tubercolosis_history = models.BooleanField()
	a4f_cronic_cough_history = models.BooleanField()
	a4f_hypertension_history = models.BooleanField()
	a4f_heart_disease_history = models.BooleanField()
	a4f_heart_disease_coronary = models.BooleanField()
	a4f_heart_disease_valve = models.BooleanField()
	a4f_heart_disease_rhythm = models.BooleanField()
	a4f_heart_disease_muscle = models.BooleanField()
	a4f_diabetes_history = models.BooleanField()
	a4f_is_use_insulin = models.BooleanField()
	a4f_stroke_history = models.BooleanField()
	a4f_allergy_history = models.BooleanField()
	a4f_allergy_detail = models.CharField(max_length=25)
	a4f_other_history = models.BooleanField()
	a4f_other_detail = models.CharField(max_length=25)
	a4f_family_disease = models.BooleanField()
	a4f_asthma_mother = models.BooleanField()
	a4f_asthma_father = models.BooleanField()
	a4f_asthma_sibling = models.BooleanField()
	a4f_hypertension_mother = models.BooleanField()
	a4f_hypertension_father = models.BooleanField()
	a4f_hypertension_sibling = models.BooleanField()
	a4f_heart_disease_mother = models.BooleanField()
	a4f_heart_disease_father = models.BooleanField()
	a4f_heart_disease_sibling = models.BooleanField()
	a4f_diabetes_mother = models.BooleanField()
	a4f_diabetes_father = models.BooleanField()
	a4f_diabetes_sibling = models.BooleanField()
	a4f_stroke_mother = models.BooleanField()
	a4f_stroke_father = models.BooleanField()
	a4f_stroke_sibling = models.BooleanField()
	a4f_other_disease = models.BooleanField()
	a4f_other_disease_name = models.CharField(max_length=25)
	a4f_other_mother = models.BooleanField()
	a4f_other_father = models.BooleanField()
	a4f_other_sibling = models.BooleanField()


class A5PrePregnancySmoking(models.Model):
	a_form = models.ForeignKey(ABaseLine, on_delete=models.PROTECT)
	SMOKING_STATUS_LIST = (
					('1', 'Smoker'),
					('2', 'Ex-smoker'),
					('3', 'Never smoke'),
		)
	a5m_mother_smoking_status = models.CharField(choices=SMOKING_STATUS_LIST, max_length=1, default="")
	a5m_mother_quit_duration = models.IntegerField(null=True)
	a5m_mother_start_smoke_age = models.IntegerField(null=True)
	a5m_mother_cigarretes_per_day = models.IntegerField(null=True)
	a5m_mother_smoke_pipes = models.BooleanField()
	a5m_other_member_smoke = models.BooleanField()
	a5m_other_member_smoke_number = models.IntegerField(null=True)
	a5m_total_cigarretes_per_day = models.IntegerField(null=True)
	a5m_smoke_in_front_of = models.BooleanField()
	##
	a5f_father_smoking_status = models.CharField(choices=SMOKING_STATUS_LIST, max_length=1, default="")
	a5f_father_quit_duration = models.IntegerField(null=True)
	a5f_father_start_smoke_age = models.IntegerField(null=True)
	a5f_father_cigarretes_per_day = models.IntegerField(null=True)
	a5f_father_smoke_pipes = models.BooleanField()
	SMOKING_FREQUENCY_LIST = (
						('1','Daily'),
						('2','Weekly'),
						('3', 'Monthly'),
						('0','Never'),
		)
	a5f_father_smoke_frequency = models.CharField(choices=SMOKING_FREQUENCY_LIST, max_length=1, default="")
	a5f_smoke_in_front_of_mother = models.BooleanField()
	###
	a5c_colleagues_smoking_status = models.CharField(choices=SMOKING_STATUS_LIST, max_length=1, default="")
	a5c_colleagues_smoke = models.IntegerField(null=True)
	a5c_duration_with_smokers_per_day = models.IntegerField(null=True)
	a5c_month_duration_with_smokers = models.IntegerField(null=True) 