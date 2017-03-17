from __future__ import unicode_literals
from django.db import models
from core.models import *
from django.db import IntegrityError

class CBirth(models.Model):
	participant = models.ForeignKey(Participant, on_delete=models.PROTECT)
	child_id = models.CharField(max_length=25)
	interviewer_id = models.CharField(max_length=25)
	data_entry_id = models.CharField(max_length=25)
	data_checked_id = models.CharField(max_length=25, null=True)
	date_admission = models.DateField()
	date_interviewed = models.DateField()
	date_data_entered = models.DateField()
	date_data_checked = models.DateField(null=True)
	is_save_all = models.BooleanField(default=False)	


class CMother(models.Model):	
	c_form = models.ForeignKey(CBirth, on_delete=models.PROTECT)	
	c1m_ur_number = models.CharField(max_length=25)
	c1m_delivery_place = models.CharField(max_length=25)
	c1m_gestational_age_fdlm = models.CharField(max_length=25)
	c1m_gestational_age_usg = models.CharField(max_length=25)
	c1m_systolic1st = models.CharField(max_length=25)
	c1m_systolic2nd = models.CharField(max_length=25)
	c1m_diastolic1st = models.CharField(max_length=25)
	c1m_diastolic2nd = models.CharField(max_length=25)
	c1m_delivery_weight = models.CharField(max_length=25)
	DELIVERY_METHOD_LIST = (
					('1', 'Unassisted vaginal birth'),
					('2', 'vacuum'),
					('3', 'Forceps'),
					('4', 'C-section'),
	)
	c1m_delivery_method = models.CharField(choices=DELIVERY_METHOD_LIST, max_length=1, default="")
	DELIVERY_COMPILATION_OPTION = (
		('0', 'No'),
		('1', 'Yes'),
	)
	c1m_delivery_compilation = models.CharField(choices=DELIVERY_COMPILATION_OPTION, max_length=1, default="")
	c1m_hypertensioncom = models.BooleanField(default=False)
	c1m_eclampsiacom = models.BooleanField(default=False)
	c1m_visualcom = models.BooleanField(default=False)
	c1m_consciousnesscom = models.BooleanField(default=False)
	c1m_seizurecom = models.BooleanField(default=False)
	c1m_pullmonarycom = models.BooleanField(default=False)
	c1m_postpartumcom = models.BooleanField(default=False)
	c1m_fevercom = models.BooleanField(default=False)
	c1m_prematurerupturecom = models.BooleanField(default=False)
	c1m_placentacom = models.BooleanField(default=False)
	c1m_placenta_previacom = models.BooleanField(default=False)
	c1m_gbscom = models.BooleanField(default=False)
	c1m_chorioamnionitiscom = models.BooleanField(default=False)
	c1m_chlinical_diagnosiscom = models.BooleanField(default=False)
	c1m_definite_diagnosiscom = models.BooleanField(default=False)
	c1m_othercom = models.CharField(max_length=25, default="", null=True)
	c1m_antibiotics = models.BooleanField(default=False)
	c1m_antibiotics_type = models.CharField(max_length=25, null=True)
	c1m_antibiotics_indication = models.CharField(max_length=255, null=True)
	c1m_antibiotics_duration = models.CharField(max_length=20, null=True)
	PROTEINURIA_OPTION = (
		('0', 'Negative'),
		('1', 'Positive +'),
		('2', 'Positive ++'),
		('3', 'Positive +++'),
	)
	c1m_proteinuria = models.CharField(choices=PROTEINURIA_OPTION, max_length=1, default="");
	c1m_delivery_blood_test = models.BooleanField()
	c1m_blood_test_date = models.DateField()	 
	c1m_hb = models.DecimalField(max_digits=10, decimal_places=3, null=True)
	c1m_wbc = models.DecimalField(max_digits=10, decimal_places=3, null=True)
	c1m_platelets = models.DecimalField(max_digits=10, decimal_places=3, null=True)
	c1m_sgot = models.DecimalField(max_digits=10, decimal_places=3, null=True)
	c1m_sgpt = models.DecimalField(max_digits=10, decimal_places=3, null=True)
	c1m_ureum = models.DecimalField(max_digits=10, decimal_places=3, null=True)
	c1m_creatinine = models.DecimalField(max_digits=10, decimal_places=3, null=True)
	c1m_vaginal_swab = models.BooleanField()
	c1m_swab_date = models.DateField()


class CPlacentalSampling(models.Model):
	c_form = models.ForeignKey(CBirth, on_delete=models.PROTECT)
	c2m_sampling_date = models.DateField()
	c2m_sampling_time = models.TimeField();
	c2m_pictures_taken = models.BooleanField()
	c2m_comments = models.BooleanField()
	PLACENTA_SHAPES = (
		('1', 'Ellipse'),
		('2', 'Oval'),
		('3', 'Other'),
	)
	c2m_placenta_shapes = models.CharField(choices=PLACENTA_SHAPES, max_length=1, default="")
	c2m_placenta_other = models.CharField(max_length=100)
	UMBILICAL_CORD = (
		('1', 'Centre'),
		('2', 'Marginal'),
	)
	c2m_umbilical_cord = models.CharField(choices=UMBILICAL_CORD, max_length=1, default="")
	c2m_abnormality = models.CharField(max_length=100)
	c2m_cord_blood_sample = models.BooleanField()
	c2m_membrane_roll = models.BooleanField()
	c2m_membrane_trim = models.BooleanField()
	c2m_membrane_weight = models.CharField(max_length=5)
	c2m_villous_tissue = models.BooleanField()
	c2m_placenta_container = models.BooleanField()
	c2m_placenta_laboratory = models.BooleanField()
	c2m_placenta_sampling = models.BooleanField()


class CInfantData(models.Model):
	c_form = models.ForeignKey(CBirth, on_delete=models.PROTECT)
	c3c_ur_number = models.CharField(max_length=25)
	c3c_first_name = models.CharField(max_length=25)
	c3c_surname = models.CharField(max_length=25)
	c3c_dob = models.DateField()
	SEX_LIST = (
		('1', 'male'),
		('2', 'female'),
		('3', 'indetermined'),	
	)
	c3c_sex = models.CharField(choices=SEX_LIST, max_length=1, default="")
	PLURALITY_LIST = (
		('1', 'Single'),
		('2', 'Twin'),
	)
	c3c_plurality = models.CharField(choices=PLURALITY_LIST, max_length=1, default="")
	c3c_preterm = models.BooleanField()
	c3c_ballad_score = models.CharField(max_length=25)
	c3c_birth_weight_1st = models.CharField(max_length=25)
	c3c_birth_weight_2nd = models.CharField(max_length=25)
	c3c_birth_length_1st = models.CharField(max_length=25)
	c3c_birth_length_2nd = models.CharField(max_length=25)
	c3c_hc_1st = models.CharField(max_length=25)
	c3c_hc_2nd = models.CharField(max_length=25)
	c3c_still_birth = models.BooleanField()
	c3c_apgar1 = models.CharField(max_length=25)
	c3c_apgar5 = models.CharField(max_length=25)
	c3c_failure_respiration = models.BooleanField()
	c3c_resuscitation = models.BooleanField()
	c3c_oxygen_therapy = models.BooleanField()
	c3c_air_cpap = models.BooleanField()
	c3c_oxygen_cpap = models.BooleanField()
	c3c_air_ippr = models.BooleanField()
	c3c_oxygen_ippr = models.BooleanField()
	c3c_air_intubation = models.BooleanField()
	c3c_oxygen_intubation = models.BooleanField()
	c3c_cardiac_massage = models.BooleanField()
	c3c_resuscitation_drug = models.BooleanField()
	c3c_drug_name = models.CharField(max_length=50)
	c3c_drug_dose = models.CharField(max_length=25)
	c3c_nursery_care = models.BooleanField()
	c3c_duration_nursery_care = models.CharField(max_length=25)
	c3c_nicu = models.BooleanField()
	c3c_duration_nicu = models.CharField(max_length=25)
	c3c_neonatal_morbidity = models.BooleanField()
	c3c_sepsis = models.BooleanField()
	c3c_sepsis_presumed = models.BooleanField()
	c3c_sepsis_definite = models.BooleanField()
	c3c_sepsis_bacteria1 = models.CharField(max_length=50)
	c3c_sepsis_bacteria2 = models.CharField(max_length=50)
	c3c_sepsis_drug1 = models.CharField(max_length=50)
	c3c_sepsis_drug2 = models.CharField(max_length=50)
	c3c_sepsis_dose1 = models.CharField(max_length=50)
	c3c_sepsis_dose2 = models.CharField(max_length=50)
	c3c_sepsis_frequency1 = models.CharField(max_length=50)
	c3c_sepsis_frequency2 = models.CharField(max_length=50)
	c3c_sepsis_duration1 = models.CharField(max_length=50)
	c3c_sepsis_duration2 = models.CharField(max_length=50)
	c3c_iterus = models.BooleanField()
	c3c_asphyxia = models.BooleanField()
	c3c_respiratory_distress = models.BooleanField()
	# RESPIRATORIES_LIST = (
	# 	('1', 'Nenatal pneumonia'),
	# 	('2', 'Hyaline membrane disease'),
	# 	('3', 'Meconium aspiration syndrome'),
	# 	('4', 'others'),		
	# )
	c3c_respiratory_diagnosis = models.CharField( max_length=1, default="")
	c3c_other_respiratory_diagnosis = models.CharField(max_length=25)
	# RESPIRATORY_SUPPORT_LIST = (
	# 	('1', '02 therapy (nasal/mask)'),
	# 	('2', 'CPAP'),
	# 	('3', 'Non-invasive IPPR'),
	# 	('4', 'Intubation/ETT'),
	# )
	c3c_respiratory_support = models.CharField(max_length=1, default="")
	c3c_others_mobirdities = models.CharField(max_length=25)
	c3c_congenital_anomaly = models.BooleanField()
	c3c_cardiovascularano = models.BooleanField()
	c3c_cnsano = models.BooleanField()
	c3c_musculoskeletalano = models.BooleanField()
	c3c_gastrointestinalano = models.BooleanField()
	c3c_urogenitalano = models.BooleanField()
	c3c_respiratoryano = models.BooleanField()
	c3c_skinano = models.BooleanField()
	c3c_down_syndromeano = models.BooleanField()
	c3c_other_syndromeano = models.CharField(max_length=50)
	c3c_congenital_infection = models.BooleanField()
	c3c_toxoplasmosisinf = models.BooleanField()
	c3c_rubellainf = models.BooleanField()
	c3c_cytomegalovirusinf = models.BooleanField()
	c3c_syphillisinf = models.BooleanField()
	c3c_hivinf = models.BooleanField()
	c3c_hiv_prevention = models.BooleanField()
	c3c_blood_test_septic = models.BooleanField()
	c3c_blood_test_date = models.DateField()
	c3c_hb_septic = models.CharField(max_length=10)
	c3c_wbc_septic = models.CharField(max_length=10)
	c3c_platelet_septic = models.CharField(max_length=10)
	c3c_crp_septic = models.CharField(max_length=10)
	c3c_ITRatio_septic = models.CharField(max_length=10)
	c3c_coord_blood_analysis = models.BooleanField()
	c3c_pH = models.IntegerField(null=True)
	c3c_po2 = models.IntegerField(null=True)
	c3c_pco2 = models.IntegerField(null=True)
	c3c_hco3 = models.IntegerField(null=True)
	c3c_base_excess = models.IntegerField(null=True)
	c3c_coord_blood_sampling = models.BooleanField()
	c3c_cord_blood_date = models.DateField()
	c4m_discharge_date = models.DateField()
	c4c_discharge_date = models.DateField()















	
