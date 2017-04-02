from __future__ import unicode_literals

from django.db import models

# Create your models here.


class BPregnancy(models.Model):
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


class B1MedicalData(models.Model):
	b1_form = models.ForeignKey(BPregnancy, on_delete=models.PROTECT)
	b1m_weight = models.DecimalField(decimal_places=1)
	b1m_fundal = models.DecimalField(decimal_places=1)
	b1m_systolic1st = models.IntegerField()
	b1m_systolic2nd = models.IntegerField()
	b1m_diastolic1st = models.IntegerField()
	b1m_diastolic2nd = models.IntegerField()
	b1m_complication = models.BooleanField()
	b1m_hypertensioncom = models.BooleanField()
	b1m_visualcom = models.BooleanField()
	b1m_consciousnesscom = models.BooleanField()
	b1m_seizurecom = models.BooleanField()
	b1m_diabetescom = models.BooleanField()
	b1m_eclampsiacom = models.BooleanField()
	b1m_laborcom = models.BooleanField()
	b1m_hypremesiscom = models.BooleanField()
	b1m_tbcom = models.BooleanField()
	b1m_hivcom = models.BooleanField()
	b1m_urinarycom = models.BooleanField()
	b1m_fevercom = models.BooleanField()
	b1m_respiratorycom = models.BooleanField()
	b1m_pulmonarycom = models.BooleanField()
	b1m_chroniccom = models.BooleanField()
	b1m_gastroentetriscom = models.BooleanField()
	b1m_other = models.CharField(max_length=50)

class B1UltrasoundScanResults(models.Model):
	b2m_date_exam = models.DateField()
	b2m_gestat_age = models.IntegerField()
	b2m_hc = models.DecimalField(decimal_places=2)
	b2m_bd = models.DecimalField(decimal_places=2)
	b2m_fl = models.DecimalField(decimal_places=2)
	b2m_di = models.DecimalField(decimal_places=2)
	b2m_conanomaly = models.BooleanField()
	b2m_conanomaly_specify = models.CharField(max_length=50)
	b2m_SVDoppler = models.DecimalField(decimal_places=2)
	b2m_DVDoppler = models.DecimalField(decimal_places=2)
	b2m_rimca = models.CharField()
	b2m_amnion = models.DecimalField(decimal_places=2)


class B1LaboratoryTest(models.Model):
	b3m_date_urin = models.DateField()
	PROTEINURIA_LIST = (
		('1', 'positif+'),
		('2', 'positif++'),
		('3', 'positif+++'),
		('0', 'negative'),
	)
	b3m_proteinuria = models.CharField(choices=PROTEINURIA_LIST, max_length=1, default="")
	b3m_blood_test =  models.BooleanField()
	b3m_date_blood = models.DateField()
	b3m_rbc = models.DecimalField()
	b3m_hb = models.DecimalField()
	b3m_wbc = models.DecimalField()
	b3m_thrombocyte = models.DecimalField()
	b3m_SGOT = models.IntegerField()
	b3m_SGPT = models.IntegerField()
	b3m_thrombocyte = models.IntegerField()
	b3m_ureum = models.IntegerField()
	b3m_creatinine = models.IntegerField()
	b3m_hiv_date = models.DateField()
	b3m_hiv_status = models.BooleanField()
	b3m_hepB_test = models.BooleanField()
	b3m_hepB_date = models.DateField()
	b3m_hepB_status = models.BooleanField()
	b3m_torch_test = models.BooleanField()
	b3m_torch_date = models.DateField()
	b3m_torch_status = models.BooleanField()	
	TORCH_LIST = (
		('1', 'Ig G'),
		('2', 'Ig M'),
		('0', 'No'),
	)
	b3m_toxo = models.CharField(choices=TORCH_LIST, max_length=1, default="")
	b3m_rubella = models.CharField(choices=TORCH_LIST, max_length=1, default="")
	b3m_cmv = models.CharField(choices=TORCH_LIST, max_length=1, default="")
	b3m_herpes = models.CharField(choices=TORCH_LIST, max_length=1, default="")
	b3m_urin_date = models.DateField()
	b3m_blood_date = models.DateField()
	b3m_stool_date = models.DateField()
	b3m_hair_date = models.DateField()
	b3m_nail_date = models.DateField()
	b3m_lung_date = models.DateField()
	b3m_FVC1st = models.DecimalField()
	b3m_FVC2nd = models.DecimalField()
	b3m_FVC3rd = models.DecimalField()
	b3m_FEV11st = models.DecimalField()
	b3m_FEV12nd = models.DecimalField()
	b3m_FEV13rd = models.DecimalField()
	b3m_FEV31st = models.DecimalField()
	b3m_FEV32nd = models.DecimalField()
	b3m_FEV33rd = models.DecimalField()
	b3m_PEF1st = models.DecimalField()
	b3m_PEF2nd = models.DecimalField()
	b3m_PEF3rd = models.DecimalField()
	b3m_FEF25751st = models.DecimalField()
	b3m_FEF25752nd = models.DecimalField()
	b3m_FEF25753rd = models.DecimalField()


class B4CurrentSmookingHabits(models.Model):
	SMOKING_STATUS = (
		('1', 'Smoker'),
		('2', 'Ex-smoker'),
		('3', 'Never smoke'),
	)
	b4m_smoking_status = models.CharField(choices=SMOKING_STATUS, max_length=1, default="")
	b4m_quitting_duration = models.IntegerField()
	b4m_smoking_status = models.CharField(max_length=4)
	b4m_cigar_type = models.BooleanField()
	b4m_household_smoker = models.BooleanField()
	b4m_household_smoker_number = models.CharField(max_length=3)
	b4m_household_total_cigar = models.IntegerField()
	b4m_household_presence = models.BooleanField()






