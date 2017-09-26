from __future__ import unicode_literals
from django.db import models
from core.models import *
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from datetime import datetime
# Create your models here.


class B2Pregnancy(models.Model):

	def __str__(self):
		return unicode(self.participant)
		
	participant = models.ForeignKey(Participant, on_delete=models.PROTECT)	
	interviewer_id = models.CharField(max_length=25, null=True, blank=True)
	data_entry_id = models.CharField(max_length=25, null=True, blank=True)
	data_checked_id = models.CharField(max_length=25, blank=True, null=True)
	date_admission = models.CharField(max_length=10, blank=True, null=True)
	date_interviewed = models.CharField(max_length=10, blank=True, null=True)
	date_data_entered = models.CharField(max_length=10, blank=True, null=True)
	date_data_checked = models.CharField(max_length=10, blank=True, null=True)
	is_save_all = models.BooleanField(default=False)


class B2MedicalData(models.Model):

	def __str__(self):
		return "[participant_id : " + unicode(self.participant_id)+ ", name : "+unicode(self.b1_form.participant.name)+"]" 

	b1_form = models.ForeignKey(B2Pregnancy, on_delete=models.PROTECT)
	participant_id = models.CharField(max_length=10, null=True, blank=True)
	created_time = models.CharField(max_length=50, null=True, blank=True)
	updated_time = models.CharField(max_length=50, null=True, blank=True)
	data_entry_id = models.CharField(max_length=25, null=True, blank=True)
	data_updated_id = models.CharField(max_length=25, null=True, blank=True)
	b1m_weight = models.CharField(max_length=10, null=True, blank=True)
	b1m_fundal =  models.CharField(max_length=10, null=True, blank=True)
	b1m_systolic1st = models.CharField(max_length=10, null=True, blank=True)
	b1m_systolic2nd = models.CharField(max_length=10, null=True, blank=True)
	b1m_diastolic1st = models.CharField(max_length=10, null=True, blank=True)
	b1m_diastolic2nd = models.CharField(max_length=10, null=True, blank=True)
	b1m_complication = models.NullBooleanField(default=False, blank=True)
	b1m_hypertensioncom = models.BooleanField(default=False, blank=True)
	b1m_visualcom = models.BooleanField(default=False, blank=True)
	b1m_consciousnesscom = models.BooleanField(default=False, blank=True)
	b1m_seizurecom = models.BooleanField(default=False, blank=True)
	b1m_diabetescom = models.BooleanField(default=False, blank=True)
	b1m_eclampsiacom = models.BooleanField(default=False, blank=True)
	b1m_laborcom = models.BooleanField(default=False, blank=True)
	b1m_hypremesiscom = models.BooleanField(default=False, blank=True)
	b1m_tbcom = models.BooleanField(default=False, blank=True)
	b1m_hivcom = models.BooleanField(default=False, blank=True)
	b1m_urinarycom = models.BooleanField(default=False, blank=True)
	b1m_fevercom = models.BooleanField(default=False, blank=True)
	b1m_respiratorycom = models.BooleanField(default=False, blank=True)
	b1m_pulmonarycom = models.BooleanField(default=False, blank=True)
	b1m_chroniccom = models.BooleanField(default=False, blank=True)
	b1m_gastroentetriscom = models.BooleanField(default=False, blank=True)
	b1m_other = models.CharField(max_length=50, null=True, blank=True)
	b1m_notes = models.CharField(max_length=1000, null=True, blank=True)
	

class B2UltrasoundScanResults(models.Model):

	def __str__(self):
		return "[participant_id : " + unicode(self.participant_id)+ ", name : "+unicode(self.b1_form.participant.name)+"]" 

	b1_form = models.ForeignKey(B2Pregnancy, on_delete=models.PROTECT)
	participant_id = models.CharField(max_length=10, null=True, blank=True)
	created_time = models.CharField(max_length=50, null=True, blank=True)
	updated_time = models.CharField(max_length=50, null=True, blank=True)
	data_entry_id = models.CharField(max_length=25, null=True, blank=True)
	data_updated_id = models.CharField(max_length=25, null=True, blank=True)
	b2m_date_exam = models.CharField(max_length=10, blank=True, null=True)	
	b2m_gestat_age = models.CharField(max_length=5, blank=True, null=True)
	b2m_hc = models.CharField(max_length=10, blank=True, null=True)
	b2m_ac = models.CharField(max_length=10, blank=True)
	b2m_bd = models.CharField(max_length=10, blank=True)
	b2m_fl = models.CharField(max_length=10, blank=True)
	b2m_di = models.CharField(max_length=10, blank=True)
	b2m_conanomaly = models.NullBooleanField(blank=True)
	b2m_conanomaly_specify = models.CharField(max_length=50, blank=True, default="", null=True)
	b2m_SVDoppler = models.CharField(max_length=10, blank=True)
	b2m_DVDoppler = models.CharField(max_length=10, blank=True)
	b2m_sd_ratio =  models.CharField(max_length=10, blank=True)
	b2m_rimca = models.CharField(max_length=10, blank=True)
	b2m_amnion = models.CharField(max_length=10, blank=True)
	b2m_notes = models.CharField(max_length=1000, null=True, blank=True)


class B2LaboratoryTest(models.Model):
	def __str__(self):
		return "[participant_id : " + unicode(self.participant_id)+ ", name : "+unicode(self.b1_form.participant.name)+"]"

	b1_form = models.ForeignKey(B2Pregnancy, on_delete=models.PROTECT)
	participant_id = models.CharField(max_length=10, null=True, blank=True)
	created_time = models.CharField(max_length=50, null=True, blank=True)
	updated_time = models.CharField(max_length=50, null=True, blank=True)
	data_entry_id = models.CharField(max_length=25, null=True, blank=True)
	data_updated_id = models.CharField(max_length=25, null=True, blank=True)
	b3m_date_urin = models.CharField(max_length=10, blank=True, null=True)
	PROTEINURIA_LIST = (
		('', ''),
		('1', 'positif+'),
		('2', 'positif++'),
		('3', 'positif+++'),
		('0', 'negative'),
	)
	b3m_proteinuria = models.CharField(choices=PROTEINURIA_LIST, max_length=1, default="", null=True)
	b3m_blood_test =  models.NullBooleanField(default=False)
	b3m_date_blood = models.CharField(max_length=10, blank=True, null=True)
	b3m_hb = models.CharField(max_length=10, null=True, blank=True)
	b3m_rbc = models.CharField(max_length=10, null=True, blank=True)
	b3m_wbc = models.CharField(max_length=10, null=True, blank=True)
	b3m_thrombocyte = models.CharField(max_length=10, null=True, blank=True)
	b3m_SGOT = models.CharField(max_length=10, null=True, blank=True)
	b3m_SGPT = models.CharField(max_length=10, null=True, blank=True)	
	b3m_ureum = models.CharField(max_length=10, null=True, blank=True)
	b3m_creatinine = models.CharField(max_length=10, null=True, blank=True)
	b3m_hiv_test = models.NullBooleanField(default=False, blank=True)
	b3m_hiv_date = models.CharField(max_length=10, blank=True, null=True)
	b3m_hiv_status = models.NullBooleanField(default=False, blank=True)
	b3m_hepB_test = models.NullBooleanField(default=False, blank=True)
	b3m_hepB_date = models.CharField(max_length=10, blank=True, null=True)
	b3m_hepB_status = models.NullBooleanField(default=False, blank=True)
	b3m_torch_test = models.NullBooleanField(default=False, blank=True)
	b3m_torch_date = models.CharField(max_length=10, blank=True, null=True)
	#b3m_torch_status = models.BooleanField()	
	TORCH_LIST = (
		('', ''),
		('1', 'Ig G'),
		('2', 'Ig M'),
		('0', 'No'),
	)
	b3m_toxo = models.CharField(choices=TORCH_LIST, max_length=1, default="", null=True, blank=True)
	b3m_rubella = models.CharField(choices=TORCH_LIST, max_length=1, default="", null=True)
	b3m_cmv = models.CharField(choices=TORCH_LIST, max_length=1, default="", null=True, blank=True)
	b3m_herpes = models.CharField(choices=TORCH_LIST, max_length=1, default="", null=True, blank=True)
	b3m_urin_date = models.CharField(max_length=10, blank=True, null=True)
	b3m_blood_date = models.CharField(max_length=10, blank=True, null=True)
	b3m_stool_date = models.CharField(max_length=10, blank=True, null=True)
	b3m_hair_date = models.CharField(max_length=10, blank=True, null=True)
	b3m_nail_date = models.CharField(max_length=10, blank=True, null=True)
	b3m_lung_date = models.CharField(max_length=10, blank=True, null=True)
	b3m_FVC1st = models.CharField(max_length=20, null=True, blank=True)
	b3m_FVC2nd = models.CharField(max_length=20, null=True, blank=True)
	b3m_FVC3rd = models.CharField(max_length=20, null=True, blank=True)
	b3m_FEV11st = models.CharField(max_length=20, null=True, blank=True)
	b3m_FEV12nd = models.CharField(max_length=20, null=True, blank=True)
	b3m_FEV13rd = models.CharField(max_length=20, null=True, blank=True)
	b3m_FEV31st = models.CharField(max_length=20, null=True, blank=True)
	b3m_FEV32nd = models.CharField(max_length=20, null=True, blank=True)
	b3m_FEV33rd = models.CharField(max_length=20, null=True, blank=True)
	b3m_PEF1st = models.CharField(max_length=20, null=True, blank=True)
	b3m_PEF2nd = models.CharField(max_length=20, null=True, blank=True)
	b3m_PEF3rd = models.CharField(max_length=20, null=True, blank=True)
	b3m_FEF25751st = models.CharField(max_length=20, null=True, blank=True)
	b3m_FEF25752nd = models.CharField(max_length=20, null=True, blank=True)
	b3m_FEF25753rd = models.CharField(max_length=20, null=True, blank=True)
	b3m_notes = models.CharField(max_length=1000, null=True, blank=True)

# #Telah memulai perbaikan dari class di bawah ini
class B2CurrentSmookingHabits(models.Model):

	def __str__(self):
		return "[participant_id : " + unicode(self.participant_id)+ ", name : "+unicode(self.b1_form.participant.name)+"]" 

	b1_form = models.ForeignKey(B2Pregnancy, on_delete=models.PROTECT)
	participant_id = models.CharField(max_length=10, null=True, blank=True)
	created_time = models.CharField(max_length=50, null=True, blank=True)
	updated_time = models.CharField(max_length=50, null=True, blank=True)
	data_entry_id = models.CharField(max_length=25, null=True, blank=True)
	data_updated_id = models.CharField(max_length=25, null=True, blank=True)
	SMOKING_STATUS = (
		('', ''),
		('1', 'Smoker'),
		('2', 'Ex-smoker'),
		('0', 'Never smoke'),
	)
	b4m_smoking_status = models.CharField(choices=SMOKING_STATUS, max_length=1, blank=True)
	b4m_quitting_duration = models.CharField(max_length=20, null=True, blank=True)
	b4m_cigar_type = models.NullBooleanField(default=False, blank=True)
	b4m_cigar_number = models.CharField(max_length=20, null=True, blank=True)
	b4m_household_smoker = models.NullBooleanField(default=False, blank=True)
	b4m_household_smoker_number = models.CharField(max_length=3, blank=True, null=True)
	b4m_household_total_cigar = models.CharField(max_length=5, blank=True, null=True)
	b4m_household_presence = models.NullBooleanField(default=False, blank=True, null=True)
	b4f_smoking_status = models.CharField(choices=SMOKING_STATUS, max_length=1, default="", blank=True)
	b4f_quitting_duration = models.CharField(max_length=20, null=True, blank=True)
	b4f_cigar_number = models.CharField(max_length=20, null=True, blank=True)
	b4f_cigar_type = models.NullBooleanField(default=False, blank=True)

	SMOKING_FREQUENCY = (
		('', ''),
		('1', 'Daily'),
		('2', 'Weekly'),
		('3', 'Monthly'),
		('0', 'Never')
	)
	b4f_smoking_inside_house = models.CharField(choices=SMOKING_FREQUENCY, max_length=1, default="", blank=True, null=True)
	b4f_smoking_presence = models.NullBooleanField(default=False, blank=True, null=True)
	b4c_smoking_presence = models.NullBooleanField(default=False, blank=True, null=True)
	b4c_smoker_number = models.CharField(max_length=5, blank=True, default=0, null=True)
	b4c_daily_duration = models.CharField(max_length=5, blank=True, null=True)
	b4m_notes = models.CharField(max_length=1000, null=True, blank=True)

class B2PollutanExposure(models.Model):
	def __str__(self):
		return "[participant_id : " + unicode(self.participant_id)+ ", name : "+unicode(self.b1_form.participant.name)+"]"
	
	b1_form = models.ForeignKey(B2Pregnancy, on_delete=models.PROTECT)
	participant_id = models.CharField(max_length=10, null=True, blank=True)
	created_time = models.CharField(max_length=50, null=True, blank=True)
	updated_time = models.CharField(max_length=50, null=True, blank=True)
	data_entry_id = models.CharField(max_length=25, null=True, blank=True)
	data_updated_id = models.CharField(max_length=25, null=True, blank=True)
	b5m_charcoal = models.BooleanField(default=False, blank=True)
	b5m_kerosene = models.BooleanField(default=False, blank=True)
	b5m_wood = models.BooleanField(default=False, blank=True)
	b5m_gas = models.BooleanField(default=False, blank=True)
	b5m_electric = models.BooleanField(default=False, blank=True)	
	b5m_other_cooking_fuel = models.CharField(max_length=50, null=True, blank=True)
	b5m_exhaust = models.NullBooleanField(default=False, blank=True)
	b5m_pesticide = models.NullBooleanField(default=False, blank=True)
	FREQUENCY = (
		('', ''),
		('0', 'No'),
		('1','Once per week or less'),
		('2', 'More than once per week but not daily'),
		('3', 'Daily')
	)
	b5m_garbage_burning = models.CharField(choices=FREQUENCY, max_length=1, default="", blank=True)
	b5m_pet = models.NullBooleanField(default=False, blank=True)
	b5m_pet_specify = models.CharField(max_length=100, null=True, blank=True)
	HOUSING_TYPE_LIST = (
						('', ''),
						('1','Landed House'),
						('2', 'Flat/Apartment'),
		)
	b5m_housing_type = models.CharField(choices=HOUSING_TYPE_LIST, max_length=1, default="", null=True, blank=True)
	LANDED_HOUSE_TYPE_LIST = (
						('', ''),
						('1','One story building'),
						('2', 'More than one story building'),
		)
	b5m_landed_house_type = models.CharField(choices=LANDED_HOUSE_TYPE_LIST, max_length=1, default="", null=True, blank=True)
	b5m_apartment_level_number = models.CharField(max_length=5, null=True, blank=True)
	b5m_dampness_house = models.NullBooleanField(default=False, blank=True)
	b5m_ac = models.BooleanField(default=False, blank=True)
	b5m_fan = models.BooleanField(default=False, blank=True)
	b5m_air_filter = models.BooleanField(default=False, blank=True)
	b5m_staying_out_history = models.NullBooleanField(default=False, blank=True)

	b5m_staying_out_1st_street = models.CharField(max_length=50, null=True, blank=True)
	b5m_staying_out_1st_rt = models.CharField(max_length=50, null=True, blank=True)
	b5m_staying_out_1st_rw = models.CharField(max_length=50, null=True, blank=True)
	b5m_staying_out_1st_district = models.CharField(max_length=50, null=True, blank=True)
	b5m_staying_out_1st_city = models.CharField(max_length=50, default="", null=True, blank=True)
	b5m_staying_out_1st_zipcode = models.CharField(max_length=50, null=True, blank=True)
	b5m_staying_out_1st_duration = models.CharField(max_length=50, null=True, blank=True)

	b5m_staying_out_2nd_street = models.CharField(max_length=50, null=True, blank=True)
	b5m_staying_out_2nd_rt = models.CharField(max_length=50, null=True, blank=True)
	b5m_staying_out_2nd_rw = models.CharField(max_length=50, null=True, blank=True)
	b5m_staying_out_2nd_district = models.CharField(max_length=50, null=True, blank=True)
	b5m_staying_out_2nd_city = models.CharField(max_length=50, null=True, blank=True)
	b5m_staying_out_2nd_zipcode = models.CharField(max_length=50, null=True, blank=True)
	b5m_staying_out_2nd_duration = models.CharField(max_length=50, null=True, blank=True)
	b5m_notes = models.CharField(max_length=1000, null=True, blank=True)

class B2GestationalNutrition(models.Model):

	def __str__(self):
		return "[participant_id : " + unicode(self.participant_id)+ ", name : "+unicode(self.b1_form.participant.name)+"]"

	b1_form = models.ForeignKey(B2Pregnancy, on_delete=models.PROTECT)
	participant_id = models.CharField(max_length=10, null=True, blank=True)
	created_time = models.CharField(max_length=50, null=True, blank=True)
	updated_time = models.CharField(max_length=50, null=True, blank=True)
	data_entry_id = models.CharField(max_length=25, null=True, blank=True)
	data_updated_id = models.CharField(max_length=25, null=True, blank=True)
	b6m_fasting_pregnancy = models.NullBooleanField(default=False, blank=True)
	b6m_ramadhan = models.BooleanField(default=False, blank=True)
	b6m_sunnah = models.BooleanField(default=False, blank=True)
	b6m_fasting_duration = models.IntegerField(null=True, blank=True)
	b6m_energy = models.CharField(max_length=10, null=True, blank=True)
	b6m_water = models.CharField(max_length=10, null=True, blank=True)
	b6m_protein = models.CharField(max_length=10, null=True, blank=True)
	b6m_fat = models.CharField(max_length=10, null=True, blank=True)
	b6m_carbohydrate = models.CharField(max_length=10, null=True, blank=True)
	b6m_dietary_fiber = models.CharField(max_length=10, null=True, blank=True)
	b6m_unsaturated_fat = models.CharField(max_length=10, null=True, blank=True)
	b6m_cholestrol = models.CharField(max_length=10, null=True, blank=True)
	b6m_vitA = models.CharField(max_length=10, null=True, blank=True)
	b6m_carotene = models.CharField(max_length=10, null=True, blank=True)
	b6m_vitE = models.CharField(max_length=10, null=True, blank=True)
	b6m_vitB1 = models.CharField(max_length=10, null=True, blank=True)
	b6m_vitB2 = models.CharField(max_length=10, null=True, blank=True)
	b6m_vitB6 = models.CharField(max_length=10, null=True, blank=True)
	b6m_folicAcid = models.CharField(max_length=10, null=True, blank=True)
	b6m_vitC = models.CharField(max_length=10, null=True, blank=True)
	b6m_sodium = models.CharField(max_length=10, null=True, blank=True)
	b6m_potassium = models.CharField(max_length=10, null=True, blank=True)
	b6m_calcium = models.CharField(max_length=10, null=True, blank=True)
	b6m_magnesium = models.CharField(max_length=10, null=True, blank=True)
	b6m_phosporus = models.CharField(max_length=10, null=True, blank=True)
	b6m_iron = models.CharField(max_length=10, null=True, blank=True)
	b6m_zinc = models.CharField(max_length=10, null=True, blank=True)
	FREQUENCY = (
		('', ''),
 		('1', 'Daily'),
 		('2', 'Weekly'),
 		('3', 'Monthly'),
 		('0', 'Never')
 	)
 	b6m_tea = models.CharField(choices=FREQUENCY, max_length=1, default="", blank=True)
 	b6m_coffee = models.CharField(choices=FREQUENCY, max_length=1, default="", blank=True)
 	b6m_alcohol = models.CharField(choices=FREQUENCY, max_length=1, default="", blank=True)
 	b6m_antibiotics = models.NullBooleanField(default=False, blank=True)
 	b6m_antibiotics_specify = models.CharField(max_length=25, null=True, blank=True)
 	b6m_antibiotics_duration = models.IntegerField(null=True, blank=True)
 	b6m_analgesia = models.NullBooleanField(default=False, blank=True)
 	b6m_analgesia_specify = models.CharField(max_length=25, null=True, blank=True)
 	b6m_analgesia_duration = models.IntegerField(null=True, blank=True)
 	b6m_supplement = models.NullBooleanField(default=False, blank=True)
 	b6m_supplement_specify = models.CharField(max_length=25, null=True, blank=True)
 	b6m_supplement_routine = models.NullBooleanField(default=False, blank=True)
 	b6m_supplement_duration = models.CharField(max_length=25, null=True, blank=True)
 	b6m_herbs = models.NullBooleanField(default=False, blank=True)
 	b6m_herbs_specify = models.CharField(max_length=25, null=True, blank=True)
 	b6m_herbs_routine = models.NullBooleanField(default=False, blank=True)
 	b6m_herbs_duration = models.CharField(max_length=25, null=True, blank=True)
 	b6m_other_med_exist = models.NullBooleanField(default=False, blank=True)
 	b6m_other_med = models.CharField(max_length=25, null=True, blank=True)
 	b6m_other_med_routine = models.NullBooleanField(default=False, blank=True)
 	b6m_other_med_duration = models.CharField(max_length=25, null=True, blank=True)
 	b6m_notes = models.CharField(max_length=1000, null=True, blank=True)

 	















