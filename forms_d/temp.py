d7_obj.d7c_infection = models.NullBooleanField()
	d7_obj.d7c_infection_upper_respi = models.NullBooleanField()
	d7_obj.d7c_infection_lower_respi = models.NullBooleanField()
	d7_obj.d7c_infection_gastro = models.NullBooleanField()
	d7_obj.d7c_infection_urinary = models.NullBooleanField()
	d7_obj.d7c_infection_cns = models.NullBooleanField()
	d7_obj.d7c_infection_sepsis = models.NullBooleanField()
	d7_obj.d7c_infection_dengue = models.NullBooleanField()
	d7_obj.d7c_infection_others = models.NullBooleanField()
	d7_obj.d7c_infection_unknown = models.NullBooleanField()
	d7_obj.d7c_physician_clinic = models.CharField(max_length=25)
	d7_obj.d7c_contact = models.CharField(max_length=25)
	d7_obj.d7c_infection_symptoms = models.NullBooleanField()
	d7_obj.d7c_symptoms_respi = models.NullBooleanField()
	d7_obj.d7c_symptoms_gastro = models.NullBooleanField()
	d7_obj.d7c_symptoms_skin = models.NullBooleanField()
	d7_obj.d7c_symptoms_nervous = models.NullBooleanField()
	d7_obj.d7c_hospitalization = models.NullBooleanField()
	d7_obj.d7c_admission_date = models.DateField()
	d7_obj.d7c_discharged_date = models.DateField()
	d7_obj.d7c_hospital = models.CharField(max_length=25)
	d7_obj.d7c_physician = models.CharField(max_length=25)
	d7_obj.d7c_hospital_contact = models.CharField(max_length=25)
	
	d7_obj.d7c_ward = models.CharField(choices=WARD_STATUS_LIST, max_length=1, default="")
	d7_obj.d7c_additional_test = models.NullBooleanField()
	d7_obj.d7c_blood_test = models.NullBooleanField()
	d7_obj.d7c_blood_count = models.NullBooleanField()
	d7_obj.d7c_crp = models.NullBooleanField()
	d7_obj.d7c_procalcitonin = models.NullBooleanField()
	d7_obj.d7c_blood_culture = models.NullBooleanField()
	d7_obj.d7c_blood_culture_date = models.DateField()
	d7_obj.d7c_blood_microorganism = models.CharField(max_length=25)
	d7_obj.d7c_typhoid = models.NullBooleanField()
	d7_obj.d7c_dengue_ns_1 = models.NullBooleanField()
	d7_obj.d7c_dengue = models.NullBooleanField()
	d7_obj.d7c_nasopharyngeal = models.NullBooleanField()
	d7_obj.d7c_urine = models.NullBooleanField()
	d7_obj.d7c_urinalysis = models.NullBooleanField()
	d7_obj.d7c_urinalysis_date = models.DateField()
	d7_obj.d7c_urine_culture = models.NullBooleanField()
	d7_obj.d7c_urine_date = models.DateField()
	d7_obj.d7c_urine_microorganism = models.CharField(max_length=25)
	d7_obj.d7c_csf = models.NullBooleanField()
	d7_obj.d7c_csf_date = models.DateField()
	d7_obj.d7c_csf_microorganism = models.CharField(max_length=25)
	d7_obj.d7c_faecal_culture = models.NullBooleanField()
	d7_obj.d7c_faecal_date = models.DateField()
	d7_obj.d7c_faecal_microorganism = models.CharField(max_length=25)
	d7_obj.d7c_chest_xray = models.NullBooleanField()
	d7_obj.d7c_chest_xray_findings = models.CharField(max_length=25)
	d7_obj.d7c_usg = models.NullBooleanField()
	d7_obj.d7c_usg_type = models.CharField(max_length=25)
	d7_obj.d7c_usg_date = models.DateField()
	d7_obj.d7c_usg_findings = models.CharField(max_length=25)
	d7_obj.d7c_mri = models.NullBooleanField()
	d7_obj.d7c_mri_type = models.CharField(max_length=25)
	d7_obj.d7c_mri_date = models.DateField()
	d7_obj.d7c_mri_findings = models.CharField(max_length=25)
	d7_obj.d7c_other_test = models.NullBooleanField()
	d7_obj.d7c_other_test_type = models.CharField(max_length=25)
	d7_obj.d7c_other_test_date = models.DateField()
	d7_obj.d7c_other_test_findings = models.CharField(max_length=25)
	d7_obj.d7c_medication = models.NullBooleanField()
	d7_obj.d7c_med1_name = models.CharField(max_length=25)
	d7_obj.d7c_med1_dosage = models.CharField(max_length=25)
	d7_obj.d7c_med1_start_date = models.DateField()
	d7_obj.d7c_med1_end_date = models.DateField()
	d7_obj.d7c_med2_name = models.CharField(max_length=25)
	d7_obj.d7c_med2_dosage = models.CharField(max_length=25)
	d7_obj.d7c_med2_start_date = models.DateField()
	d7_obj.d7c_med2_end_date = models.DateField()
	d7c_med3_name = models.CharField(max_length=25)
	d7c_med3_dosage = models.CharField(max_length=25)
	d7c_med3_start_date = models.DateField()
	d7c_med3_end_date = models.DateField()
	d7c_med4_name = models.CharField(max_length=25)
	d7c_med4_dosage = models.CharField(max_length=25)
	d7c_med4_start_date = models.DateField()
	d7c_med4_end_date = models.DateField()
	d7c_med5_name = models.CharField(max_length=25)
	d7c_med5_dosage = models.CharField(max_length=25)
	d7c_med5_start_date = models.DateField()
	d7c_med5_end_date = models.DateField()