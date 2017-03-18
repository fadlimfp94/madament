from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
import datetime


@login_required(login_url='core:login')
def check_form(request):
	form = DInfant.objects.get(id=request.session['form_id'])
	form.data_checked_id = request.user.username
	form.date_data_checked = datetime.date.today()
	form.save()
	return process_section1(request)

@login_required(login_url='core:login')
def save_form(request):
	form = DInfant.objects.get(id=request.session['form_id'])
	form.is_save_all = True
	form.save()
	return process_section1(request)

@login_required(login_url='core:login')
def edit_form(request):
	form = DInfant.objects.get(id=request.session['form_id'])
	form.is_save_all = False
	form.save()
	request.session['edit_mode'] = True
	section_number = request.POST.get('section_number')	
	if section_number == "2":	
		return process_section2(request)
	elif section_number == "3":
		return process_section3(request)
	elif section_number == "4":
		return process_section4(request)
	elif section_number == "5":
		return process_section5(request)
	elif section_number == "6":
		return process_section6(request)
	elif section_number == "7":
		return process_section7(request)
	elif section_number == "8":
		return process_section8(request)	
	else:
		return process_section1(request)
						

@login_required(login_url='core:login')
def create_form(request):
	if request.method == "POST":
		d_obj = DInfant()
		d_obj.participant_id = request.session['participant_id']	
		d_obj.interviewer_id = request.POST.get('interviewer_id')
		d_obj.data_entry_id = request.user.username
		d_obj.date_admission = request.POST.get('date_admission')
		d_obj.date_interviewed = request.POST.get('date_interviewed')
		d_obj.date_data_entered = request.POST.get('date_data_entered')
		d_obj.save()
		request.session['form_id'] = d_obj.id
		return process_section1(request)
	else:
		participant = Participant.objects.get(id=request.session['participant_id'])
		date_admission = participant.date_admission.strftime('%Y-%m-%d')
		staff_list = User.objects.filter(is_staff=False)
		return render(request, 'forms/form.html', {'staff_list' : staff_list, 'context' : 'create_new_form', 'participant' : participant, 'date_admission' : date_admission})

###### CONTROLLER SECTION1
@login_required(login_url='core:login')
def process_section1(request):
	if request.POST.get('form_id'):
		request.session['form_id'] = request.POST.get('form_id')
	d_form_obj = DInfant.objects.get(id=int(request.session['form_id']))
	try:
		d1_obj = D1InfantGrowth.objects.get(d_form=d_form_obj)
		return update_section1(request)	
	except:
		return create_section1(request)

@login_required(login_url='core:login')
def create_section1(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d_form_obj = DInfant.objects.get(id=request.session['form_id'])
		d1_obj = D1InfantGrowth()
		d1_obj.d_form = d_form_obj
		d1_obj = save_section1(d1_obj, request)
		return show_section1(request, True)	
	else:
		return show_section1(request, False)
		
@login_required(login_url='core:login')
def update_section1(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d1_obj = D1InfantGrowth.objects.get(d_form_id=request.session['form_id'])
		d1_obj = save_section1(d1_obj, request)
		return show_section1(request, True)	
	else:
		return show_section1(request, False)		

@login_required(login_url='core:login')
def show_section1(request, is_save):
	form = DInfant.objects.get(id=request.session['form_id'])
	participant = Participant.objects.get(id=request.session['participant_id'])
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all	
	date_interviewed = form.date_interviewed.strftime('%Y-%m-%d')
	date_data_entered = form.date_data_entered.strftime('%Y-%m-%d')
	date_admission = form.date_admission.strftime('%Y-%m-%d')
	role = ''
	if not request.user.is_staff:
		role = 'staff'
	try:
		d1_obj = D1InfantGrowth.objects.get(d_form_id=form.id) 
		#dob = d1_obj.a1m_dob.strftime('%Y-%m-%d')
		#moving_date = d1_obj.a1m_moving_date.strftime('%Y-%m-%d')
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				return render(request, 'forms/section1.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d1_obj})
			else:
				return render(request, 'forms/section1.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d1_obj})
		else:
			if is_save:	
				return render(request, 'forms/section1.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d1_obj})
			else:
				return render(request, 'forms/section1.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d1_obj})	
	except:
		return render(request, 'forms/section1.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section1(d1_obj, request):
	d1_obj.d1c_ur_number = request.POST.get('d1c_ur_number')
	d1_obj.d1c_first_name = request.POST.get('d1c_first_name')
	d1_obj.d1c_surname = request.POST.get('d1c_surname')
	d1_obj.d1c_dob = request.POST.get('d1c_dob')
	d1_obj.d1c_weight_1st = request.POST.get('d1c_weight_1st')
	d1_obj.d1c_weight_2nd = request.POST.get('d1c_weight_2nd')
	d1_obj.d1c_length_1st = request.POST.get('d1c_length_1st')
	d1_obj.d1c_length_2nd = request.POST.get('d1c_length_2nd')
	d1_obj.d1c_hc_1st = request.POST.get('d1c_hc_1st')
	d1_obj.d1c_hc_2nd = request.POST.get('d1c_hc_2nd')
	d1_obj.d1c_chest_1st = request.POST.get('d1c_chest_1st')
	d1_obj.d1c_chest_2nd = request.POST.get('d1c_chest_2nd')
	d1_obj.d1c_ac_1st = request.POST.get('d1c_ac_1st')
	d1_obj.d1c_ac_2nd = request.POST.get('d1c_ac_2nd')
	d1_obj.d1c_vaccination_history = request.POST.get('d1c_vaccination_history')
	d1_obj.d1c_bcg = request.POST.get('d1c_bcg')
	d1_obj.d1c_bcg_date = request.POST.get('d1c_bcg_dat')
	d1_obj.d1c_hep_b = request.POST.get('d1c_hep_b')
	d1_obj.d1c_hep_b_date = request.POST.get('d1c_hep_b_date')
	d1_obj.d1c_dpt = request.POST.get('d1c_dpt')
	d1_obj.d1c_dpt_date = request.POST.get('d1c_dpt_date')
	d1_obj.d1c_ipv = request.POST.get('d1c_ipv')
	d1_obj.d1c_ipv_date = request.POST.get('d1c_ipv_date')
	d1_obj.d1c_opv = request.POST.get('d1c_opv')
	d1_obj.d1c_opv_date = request.POST.get('d1c_opv_date')
	d1_obj.d1c_hib = request.POST.get('d1c_hib')
	d1_obj.d1c_hib_date = request.POST.get('d1c_hib_date')
	d1_obj.d1c_rotavirus = request.POST.get('d1c_rotavirus')
	d1_obj.d1c_rotavirus_date = request.POST.get('d1c_rotavirus_date')
	d1_obj.d1c_pneumococcus = request.POST.get('d1c_pneumococcus')
	d1_obj.d1c_pneumococcus_date = request.POST.get('d1c_pneumococcus_date')
	d1_obj.d1c_influenza = request.POST.get('d1c_influenza')
	d1_obj.d1c_influenza_date = request.POST.get('d1c_influenza_date')

	if request.user.is_staff:
		d1_obj.d_form.is_save_all = True
		d1_obj.d_form.save()
	return d1_obj


###### CONTROLLER SECTION2
@login_required(login_url='core:login')
def process_section2(request):
	if request.POST.get('form_id'):
		request.session['form_id'] = request.POST.get('form_id')
	d_form_obj = DInfant.objects.get(id=int(request.session['form_id']))
	try:
		d2_obj = D2InfantFeeding.objects.get(d_form=d_form_obj)
		return update_section2(request)	
	except:
		return create_section2(request)

@login_required(login_url='core:login')
def create_section2(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d_form_obj = DInfant.objects.get(id=request.session['form_id'])
		d2_obj = D2InfantFeeding()
		d2_obj.d_form = d_form_obj
		d2_obj = save_section2(d2_obj, request)
		return show_section2(request, True)	
	else:
		return show_section2(request, False)
		
@login_required(login_url='core:login')
def update_section2(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d2_obj = D2InfantFeeding.objects.get(d_form_id=request.session['form_id'])
		d2_obj = save_section2(d2_obj, request)
		return show_section2(request, True)	
	else:
		return show_section2(request, False)		

@login_required(login_url='core:login')
def show_section2(request, is_save):
	form = DInfant.objects.get(id=request.session['form_id'])
	participant = Participant.objects.get(id=request.session['participant_id'])
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all	
	date_interviewed = form.date_interviewed.strftime('%Y-%m-%d')
	date_data_entered = form.date_data_entered.strftime('%Y-%m-%d')
	date_admission = form.date_admission.strftime('%Y-%m-%d')
	role = ''
	if not request.user.is_staff:
		role = 'staff'
	try:
		d2_obj = D2InfantFeeding.objects.get(d_form_id=form.id) 
		#dob = d2_obj.a1m_dob.strftime('%Y-%m-%d')
		#moving_date = d2_obj.a1m_moving_date.strftime('%Y-%m-%d')
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				return render(request, 'forms/section2.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d2_obj})
			else:
				return render(request, 'forms/section2.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d2_obj})
		else:
			if is_save:	
				return render(request, 'forms/section2.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d2_obj})
			else:
				return render(request, 'forms/section2.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d2_obj})	
	except:
		return render(request, 'forms/section2.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section2(d2_obj, request):
	d2_obj.d2c_breast_feeding_status = request.POST.get('d2c_breast_feeding_status')
	d2_obj.d2c_supplementary_food = request.POST.get('d2c_breast_feeding_status')
	d2_obj.d2c_infant_formula = request.POST.get('d2c_breast_feeding_status')
	d2_obj.d2c_age_formula = request.POST.get('d2c_breast_feeding_status')
	d2_obj.d2c_cows_milk_formula = request.POST.get('d2c_breast_feeding_status')
	d2_obj.d2c_soy_formula = request.POST.get('d2c_breast_feeding_status')
	d2_obj.d2c_hypo_allergen_formula = request.POST.get('d2c_breast_feeding_status')
	d2_obj.d2c_hydrolized_formula = request.POST.get('d2c_breast_feeding_status')
	d2_obj.d2c_amino_formula = request.POST.get('d2c_breast_feeding_status')
	d2_obj.d2c_weaning_food = request.POST.get('d2c_breast_feeding_status')
	d2_obj.d2c_age_weaning_food = request.POST.get('d2c_breast_feeding_status')

	if request.user.is_staff:
		d2_obj.d_form.is_save_all = True
		d2_obj.d_form.save()
	return d2_obj

###### CONTROLLER SECTION3
@login_required(login_url='core:login')
def process_section3(request):
	if request.POST.get('form_id'):
		request.session['form_id'] = request.POST.get('form_id')
	d_form_obj = DInfant.objects.get(id=int(request.session['form_id']))
	try:
		d3_obj = D3InfantCardiovascular.objects.get(d_form=d_form_obj)
		return update_section3(request)	
	except:
		return create_section3(request)

@login_required(login_url='core:login')
def create_section3(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d_form_obj = DInfant.objects.get(id=request.session['form_id'])
		d3_obj = D3InfantCardiovascular()
		d3_obj.d_form = d_form_obj
		d3_obj = save_section3(d3_obj, request)
		return show_section3(request, True)	
	else:
		return show_section3(request, False)
		
@login_required(login_url='core:login')
def update_section3(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d3_obj = D3InfantCardiovascular.objects.get(d_form_id=request.session['form_id'])
		d3_obj = save_section3(d3_obj, request)
		return show_section3(request, True)	
	else:
		return show_section3(request, False)		

@login_required(login_url='core:login')
def show_section3(request, is_save):
	form = DInfant.objects.get(id=request.session['form_id'])
	participant = Participant.objects.get(id=request.session['participant_id'])
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all	
	date_interviewed = form.date_interviewed.strftime('%Y-%m-%d')
	date_data_entered = form.date_data_entered.strftime('%Y-%m-%d')
	date_admission = form.date_admission.strftime('%Y-%m-%d')
	role = ''
	if not request.user.is_staff:
		role = 'staff'
	try:
		d3_obj = D3InfantCardiovascular.objects.get(d_form_id=form.id) 
		#dob = d3_obj.a1m_dob.strftime('%Y-%m-%d')
		#moving_date = d3_obj.a1m_moving_date.strftime('%Y-%m-%d')
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				return render(request, 'forms/section3.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d3_obj})
			else:
				return render(request, 'forms/section3.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d3_obj})
		else:
			if is_save:	
				return render(request, 'forms/section3.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d3_obj})
			else:
				return render(request, 'forms/section3.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d3_obj})	
	except:
		return render(request, 'forms/section3.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section3(d3_obj, request):
	d3_obj.d3c_date_blood_pressure = request.POST.get('d3c_date_blood_pressure')
	d3_obj.d3c_examiner_bp = request.POST.get('d3c_examiner_bp')
	d3_obj.d3c_systolic_1st = request.POST.get('d3c_systolic_1st')
	d3_obj.d3c_systolic_2nd = request.POST.get('d3c_systolic_2nd')
	d3_obj.d3c_systolic_3rd = request.POST.get('d3c_systolic_3rd')
	d3_obj.d3c_diastolic_1st = request.POST.get('d3c_diastolic_1st')
	d3_obj.d3c_diastolic_2nd = request.POST.get('d3c_diastolic_2nd')
	d3_obj.d3c_diastolic_3rd = request.POST.get('d3c_diastolic_3rd')
	d3_obj.d3c_pulse_1st = request.POST.get('d3c_pulse_1st')
	d3_obj.d3c_pulse_2nd = request.POST.get('d3c_pulse_2nd')
	d3_obj.d3c_pulse_3rd = request.POST.get('d3c_pulse_3rd')
	d3_obj.d3c_date_echo = request.POST.get('d3c_date_echo')
	d3_obj.d3c_examiner_echo = request.POST.get('d3c_examiner_echo')
	d3_obj.d3c_cineloops = request.POST.get('d3c_cineloops')
	d3_obj.d3c_heart_abnormality = request.POST.get('d3c_heart_abnormality')
	d3_obj.d3c_lvidd_1st = request.POST.get('d3c_lvidd_1st')
	d3_obj.d3c_lvidd_2nd = request.POST.get('d3c_lvidd_2nd')
	d3_obj.d3c_lvidd_3rd = request.POST.get('d3c_lvidd_3rd')
	d3_obj.d3c_lvids_1st = request.POST.get('d3c_lvids_1st')
	d3_obj.d3c_lvids_2nd = request.POST.get('d3c_lvids_2nd')
	d3_obj.d3c_lvids_3rd = request.POST.get('d3c_lvids_3rd')
	d3_obj.d3c_ivsd_1st = request.POST.get('d3c_ivsd_1st')
	d3_obj.d3c_ivsd_2nd = request.POST.get('d3c_ivsd_2nd')
	d3_obj.d3c_ivsd_3rd = request.POST.get('d3c_ivsd_3rd')
	d3_obj.d3c_ivss_1st = request.POST.get('d3c_ivss_1st')
	d3_obj.d3c_ivss_2nd = request.POST.get('d3c_ivss_2nd')
	d3_obj.d3c_ivss_3rd = request.POST.get('d3c_ivss_3rd')
	d3_obj.d3c_lvpwd_1st = request.POST.get('d3c_lvpwd_1st')
	d3_obj.d3c_lvpwd_2nd = request.POST.get('d3c_lvpwd_2nd')
	d3_obj.d3c_lvpwd_3rd = request.POST.get('d3c_lvpwd_3rd')
	d3_obj.d3c_lvpws_1st = request.POST.get('d3c_lvpws_1st')
	d3_obj.d3c_lvpws_2nd = request.POST.get('d3c_lvpws_2nd')
	d3_obj.d3c_lvpws_3rd = request.POST.get('d3c_lvpws_3rd')
	d3_obj.d3c_lvef_1st = request.POST.get('d3c_lvef_1st')
	d3_obj.d3c_lvef_2nd = request.POST.get('d3c_lvef_2nd')
	d3_obj.d3c_lvef_3rd = request.POST.get('d3c_lvef_3rd')
	d3_obj.d3c_lvfs_1st = request.POST.get('d3c_lvfs_1st')
	d3_obj.d3c_lvfs_2nd = request.POST.get('d3c_lvfs_2nd')
	d3_obj.d3c_lvfs_3rd = request.POST.get('d3c_lvfs_3rd')
	d3_obj.d3c_tvr_1st = request.POST.get('d3c_tvr_1st')
	d3_obj.d3c_tvr_2nd = request.POST.get('d3c_tvr_2nd')
	d3_obj.d3c_tvr_3rd = request.POST.get('d3c_tvr_3rd')
	d3_obj.d3c_systolic_lv_1st = request.POST.get('d3c_systolic_lv_1st')
	d3_obj.d3c_systolic_lv_2nd = request.POST.get('d3c_systolic_lv_2nd')
	d3_obj.d3c_systolic_lv_3rd = request.POST.get('d3c_systolic_lv_3rd')
	d3_obj.d3c_diastolic_lv_1st = request.POST.get('d3c_diastolic_lv_1st')
	d3_obj.d3c_diastolic_lv_2nd = request.POST.get('d3c_diastolic_lv_2nd')
	d3_obj.d3c_diastolic_lv_3rd = request.POST.get('d3c_diastolic_lv_3rd')
	d3_obj.d3c_tapse_1st = request.POST.get('d3c_tapse_1st')
	d3_obj.d3c_tapse_2nd = request.POST.get('d3c_tapse_2nd')
	d3_obj.d3c_tapse_3rd = request.POST.get('d3c_tapse_3rd')
	d3_obj.d3c_lvwall_e_1st = request.POST.get('d3c_lvwall_e_1st')
	d3_obj.d3c_lvwall_e_2nd = request.POST.get('d3c_lvwall_e_2nd')
	d3_obj.d3c_lvwall_a_1st = request.POST.get('d3c_lvwall_a_1st')
	d3_obj.d3c_lvwall_a_2nd = request.POST.get('d3c_lvwall_a_2nd')
	d3_obj.d3c_lvwall_s_1st = request.POST.get('d3c_lvwall_s_1st')
	d3_obj.d3c_lvwall_s_2nd = request.POST.get('d3c_lvwall_s_2nd')
	d3_obj.d3c_lvseptal_e_1st = request.POST.get('d3c_lvseptal_e_1st')
	d3_obj.d3c_lvseptal_e_2nd = request.POST.get('d3c_lvseptal_e_2nd')
	d3_obj.d3c_lvseptal_a_1st = request.POST.get('d3c_lvseptal_a_1st')
	d3_obj.d3c_lvseptal_a_2nd = request.POST.get('d3c_lvseptal_a_2nd')
	d3_obj.d3c_lvseptal_s_1st = request.POST.get('d3c_lvseptal_s_1st')
	d3_obj.d3c_lvseptal_s_2nd = request.POST.get('d3c_lvseptal_s_2nd')
	d3_obj.d3c_rvwall_e_1st = request.POST.get('d3c_rvwall_e_1st')
	d3_obj.d3c_rvwall_e_2nd = request.POST.get('d3c_rvwall_e_2nd')
	d3_obj.d3c_rvwall_a_1st = request.POST.get('d3c_rvwall_a_1st')
	d3_obj.d3c_rvwall_a_2nd = request.POST.get('d3c_rvwall_a_2nd')
	d3_obj.d3c_rvwall_s_1st = request.POST.get('d3c_rvwall_s_1st')
	d3_obj.d3c_rvwall_s_2nd = request.POST.get('d3c_rvwall_s_2nd')
	d3_obj.d3c_rvseptal_e_1st = request.POST.get('d3c_rvseptal_e_1st')
	d3_obj.d3c_rvseptal_e_2nd = request.POST.get('d3c_rvseptal_e_2nd')
	d3_obj.d3c_rvseptal_a_1st = request.POST.get('d3c_rvseptal_a_1st')
	d3_obj.d3c_rvseptal_a_2nd = request.POST.get('d3c_rvseptal_a_2nd')
	d3_obj.d3c_rvseptal_s_1st = request.POST.get('d3c_rvseptal_s_1st')
	d3_obj.d3c_rvseptal_s_2nd = request.POST.get('d3c_rvseptal_s_2nd')
	d3_obj.d3c_date_vaskular = request.POST.get('d3c_date_vaskular')
	d3_obj.d3c_examiner_vaskular = request.POST.get('d3c_examiner_vaskular')
	d3_obj.d3c_cineloops_abdominal = request.POST.get('d3c_cineloops_abdominal')
	d3_obj.d3c_imt_1st = request.POST.get('d3c_imt_1st')
	d3_obj.d3c_imt_2nd = request.POST.get('d3c_imt_2nd')
	d3_obj.d3c_imt_3rd = request.POST.get('d3c_imt_3rd')
	d3_obj.d3c_sdimt_1st = request.POST.get('d3c_sdimt_1st')
	d3_obj.d3c_sdimt_2nd = request.POST.get('d3c_sdimt_2nd')
	d3_obj.d3c_sdimt_3rd = request.POST.get('d3c_sdimt_3rd')
	d3_obj.d3c_distension_1st = request.POST.get('d3c_distension_1st')
	d3_obj.d3c_distension_2nd = request.POST.get('d3c_distension_2nd')
	d3_obj.d3c_distension_3rd = request.POST.get('d3c_distension_3rd')
	d3_obj.d3c_diameter_1st = request.POST.get('d3c_diameter_1st')
	d3_obj.d3c_diameter_2nd = request.POST.get('d3c_diameter_2nd')
	d3_obj.d3c_diameter_3rd = request.POST.get('d3c_diameter_3rd')

	if request.user.is_staff:
		d3_obj.d_form.is_save_all = True
		d3_obj.d_form.save()
	return d3_obj

###### CONTROLLER SECTION4
@login_required(login_url='core:login')
def process_section4(request):
	if request.POST.get('form_id'):
		request.session['form_id'] = request.POST.get('form_id')
	d_form_obj = DInfant.objects.get(id=int(request.session['form_id']))
	try:
		d4_obj = D4InfantLungFunction.objects.get(d_form=d_form_obj)
		return update_section4(request)	
	except:
		return create_section4(request)

@login_required(login_url='core:login')
def create_section4(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d_form_obj = DInfant.objects.get(id=request.session['form_id'])
		d4_obj = D4InfantLungFunction()
		d4_obj.d_form = d_form_obj
		d4_obj = save_section4(d4_obj, request)
		return show_section4(request, True)	
	else:
		return show_section4(request, False)
		
@login_required(login_url='core:login')
def update_section4(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d4_obj = D4InfantLungFunction.objects.get(d_form_id=request.session['form_id'])
		d4_obj = save_section4(d4_obj, request)
		return show_section4(request, True)	
	else:
		return show_section4(request, False)		

@login_required(login_url='core:login')
def show_section4(request, is_save):
	form = DInfant.objects.get(id=request.session['form_id'])
	participant = Participant.objects.get(id=request.session['participant_id'])
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all	
	date_interviewed = form.date_interviewed.strftime('%Y-%m-%d')
	date_data_entered = form.date_data_entered.strftime('%Y-%m-%d')
	date_admission = form.date_admission.strftime('%Y-%m-%d')
	role = ''
	if not request.user.is_staff:
		role = 'staff'
	try:
		d4_obj = D4InfantLungFunction.objects.get(d_form_id=form.id) 
		#dob = d4_obj.a1m_dob.strftime('%Y-%m-%d')
		#moving_date = d4_obj.a1m_moving_date.strftime('%Y-%m-%d')
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				return render(request, 'forms/section4.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d4_obj})
			else:
				return render(request, 'forms/section4.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d4_obj})
		else:
			if is_save:	
				return render(request, 'forms/section4.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d4_obj})
			else:
				return render(request, 'forms/section4.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d4_obj})	
	except:
		return render(request, 'forms/section4.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section4(d4_obj, request):
	d4_obj.d4c_date_lung = request.POST.get('d4c_date_lun')
	d4_obj.d4c_examiner_lung = request.POST.get('d4c_examiner_lung')
	d4_obj.d4c_resistance_1st = request.POST.get('d4c_resistance_1st')
	d4_obj.d4c_resistance_2nd = request.POST.get('d4c_resistance_2nd ')
	d4_obj.d4c_compliance_1st = request.POST.get('d4c_compliance_1st')
	d4_obj.d4c_compliance_2nd = request.POST.get('d4c_compliance_2nd')
	d4_obj.d4c_time_constant_1st = request.POST.get('d4c_time_constant_1st')
	d4_obj.d4c_time_constant_2nd = request.POST.get('d4c_time_constant_2nd')
	d4_obj.d4c_fvc_1st = request.POST.get('d4c_fvc_1st')
	d4_obj.d4c_fvc_2nd = request.POST.get('d4c_fvc_2nd')
	d4_obj.d4c_fev_1st = request.POST.get('d4c_fev_1st')
	d4_obj.d4c_fev_2nd = request.POST.get('d4c_fev_2nd')
	d4_obj.d4c_respiratory_symptom = request.POST.get('d4c_respiratory_symptom')
	d4_obj.d4c_dry_cough = request.POST.get('d4c_dry_cough')
	d4_obj.d4c_phlegmy_cough = request.POST.get('d4c_phlegmy_cough')
	d4_obj.d4c_runny_nose = request.POST.get('d4c_runny_nose')
	d4_obj.d4c_stuffed_nose = request.POST.get('d4c_stuffed_nose')
	d4_obj.d4c_wheeze = request.POST.get('d4c_wheeze')
	d4_obj.d4c_breath_shortness = request.POST.get('d4c_breath_shortness')
	d4_obj.d4c_rattly_chest = request.POST.get('d4c_rattly_chest')
	d4_obj.d4c_snoring = request.POST.get('d4c_snoring')
	d4_obj.d4c_stridor = request.POST.get('d4c_stridor')

	if request.user.is_staff:
		d4_obj.d_form.is_save_all = True
		d4_obj.d_form.save()
	return d4_obj

###### CONTROLLER SECTION5
@login_required(login_url='core:login')
def process_section5(request):
	if request.POST.get('form_id'):
		request.session['form_id'] = request.POST.get('form_id')
	d_form_obj = DInfant.objects.get(id=int(request.session['form_id']))
	try:
		d5_obj = D5InfantBiological.objects.get(d_form=d_form_obj)
		return update_section5(request)	
	except:
		return create_section5(request)

@login_required(login_url='core:login')
def create_section5(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d_form_obj = DInfant.objects.get(id=request.session['form_id'])
		d5_obj = D5InfantBiological()
		d5_obj.d_form = d_form_obj
		d5_obj = save_section5(d5_obj, request)
		return show_section5(request, True)	
	else:
		return show_section5(request, False)
		
@login_required(login_url='core:login')
def update_section5(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d5_obj = D5InfantBiological.objects.get(d_form_id=request.session['form_id'])
		d5_obj = save_section5(d5_obj, request)
		return show_section5(request, True)	
	else:
		return show_section5(request, False)		

@login_required(login_url='core:login')
def show_section5(request, is_save):
	form = DInfant.objects.get(id=request.session['form_id'])
	participant = Participant.objects.get(id=request.session['participant_id'])
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all	
	date_interviewed = form.date_interviewed.strftime('%Y-%m-%d')
	date_data_entered = form.date_data_entered.strftime('%Y-%m-%d')
	date_admission = form.date_admission.strftime('%Y-%m-%d')
	role = ''
	if not request.user.is_staff:
		role = 'staff'
	try:
		d5_obj = D5InfantBiological.objects.get(d_form_id=form.id) 
		#dob = d5_obj.a1m_dob.strftime('%Y-%m-%d')
		#moving_date = d5_obj.a1m_moving_date.strftime('%Y-%m-%d')
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				return render(request, 'forms/section5.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d5_obj})
			else:
				return render(request, 'forms/section5.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d5_obj})
		else:
			if is_save:	
				return render(request, 'forms/section5.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d5_obj})
			else:
				return render(request, 'forms/section5.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d5_obj})	
	except:
		return render(request, 'forms/section5.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section5(d5_obj, request):
	d5_obj.d5c_date_blood = request.POST.get('d5c_date_blood')
	d5_obj.d5c_buccal_swab = request.POST.get('d5c_buccal_swab')
	d5_obj.d5c_hair_1 = request.POST.get('d5c_hair_1')
	d5_obj.d5c_hair_6 = request.POST.get('d5c_hair_6')
	d5_obj.d5c_nail_1 = request.POST.get('d5c_nail_1')
	d5_obj.d5c_nail_6 = request.POST.get('d5c_nail_6')
	d5_obj.d5c_nasopharyngeal_2 = request.POST.get('d5c_nasopharyngeal_2')
	d5_obj.d5c_nasopharyngeal_4 = request.POST.get('d5c_nasopharyngeal_4')
	d5_obj.d5c_nasopharyngeal_6 = request.POST.get('d5c_nasopharyngeal_6')

	if request.user.is_staff:
		d5_obj.d_form.is_save_all = True
		d5_obj.d_form.save()
	return d5_obj

###### CONTROLLER SECTION6
@login_required(login_url='core:login')
def process_section6(request):
	if request.POST.get('form_id'):
		request.session['form_id'] = request.POST.get('form_id')
	d_form_obj = DInfant.objects.get(id=int(request.session['form_id']))
	try:
		d6_obj = D6CurrentSmoking.objects.get(d_form=d_form_obj)
		return update_section6(request)	
	except:
		return create_section6(request)

@login_required(login_url='core:login')
def create_section6(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d_form_obj = DInfant.objects.get(id=request.session['form_id'])
		d6_obj = D6CurrentSmoking()
		d6_obj.d_form = d_form_obj
		d6_obj = save_section6(d6_obj, request)
		return show_section6(request, True)	
	else:
		return show_section6(request, False)
		
@login_required(login_url='core:login')
def update_section6(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d6_obj = D6CurrentSmoking.objects.get(d_form_id=request.session['form_id'])
		d6_obj = save_section6(d6_obj, request)
		return show_section6(request, True)	
	else:
		return show_section6(request, False)		

@login_required(login_url='core:login')
def show_section6(request, is_save):
	form = DInfant.objects.get(id=request.session['form_id'])
	participant = Participant.objects.get(id=request.session['participant_id'])
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all	
	date_interviewed = form.date_interviewed.strftime('%Y-%m-%d')
	date_data_entered = form.date_data_entered.strftime('%Y-%m-%d')
	date_admission = form.date_admission.strftime('%Y-%m-%d')
	role = ''
	if not request.user.is_staff:
		role = 'staff'
	try:
		d6_obj = D6CurrentSmoking.objects.get(d_form_id=form.id) 
		#dob = d6_obj.a1m_dob.strftime('%Y-%m-%d')
		#moving_date = d6_obj.a1m_moving_date.strftime('%Y-%m-%d')
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				return render(request, 'forms/section6.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d6_obj})
			else:
				return render(request, 'forms/section6.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d6_obj})
		else:
			if is_save:	
				return render(request, 'forms/section6.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d6_obj})
			else:
				return render(request, 'forms/section6.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d6_obj})	
	except:
		return render(request, 'forms/section6.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section6(d6_obj, request):
	d6_obj.d6m_smoking_status = request.POST.get('d6m_smoking_status')
	d6_obj.d6m_quitting_smoke = request.POST.get('d6m_quitting_smoke')
	d6_obj.d6m_quitting_duration = request.POST.get('d6m_quitting_duration')
	d6_obj.d6m_cigar_number = request.POST.get('d6m_cigar_number')
	d6_obj.d6m_cigar_type = request.POST.get('d6m_cigar_type')
	d6_obj.d6m_smoking_household = request.POST.get('d6m_smoking_household')
	d6_obj.d6m_household_number = request.POST.get('d6m_household_number')
	d6_obj.d6m_household_cigar_number = request.POST.get('d6m_household_cigar_number')
	d6_obj.d6m_household_presence = request.POST.get('d6m_household_presence')

	d6_obj.d6f_smoking_status = request.POST.get('d6f_smoking_status')
	d6_obj.d6f_quitting_duration = request.POST.get('d6f_quitting_duration')
	d6_obj.d6f_cigar_number = request.POST.get('d6f_cigar_number')
	d6_obj.d6f_cigar_type = request.POST.get('d6f_cigar_type')
	d6_obj.d6f_smoking_frequency = request.POST.get('d6f_smoking_frequency')
	d6_obj.d6f_smoking_presence = request.POST.get('d6f_smoking_presence')

	if request.user.is_staff:
		d6_obj.d_form.is_save_all = True
		d6_obj.d_form.save()
	return d6_obj

###### CONTROLLER SECTION7
@login_required(login_url='core:login')
def process_section7(request):
	if request.POST.get('form_id'):
		request.session['form_id'] = request.POST.get('form_id')
	d_form_obj = DInfant.objects.get(id=int(request.session['form_id']))
	try:
		d7_obj = D7Infection.objects.get(d_form=d_form_obj)
		return update_section7(request)	
	except:
		return create_section7(request)

@login_required(login_url='core:login')
def create_section7(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d_form_obj = DInfant.objects.get(id=request.session['form_id'])
		d7_obj = D7Infection()
		d7_obj.d_form = d_form_obj
		d7_obj = save_section7(d7_obj, request)
		return show_section7(request, True)	
	else:
		return show_section7(request, False)
		
@login_required(login_url='core:login')
def update_section7(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d7_obj = D7Infection.objects.get(d_form_id=request.session['form_id'])
		d7_obj = save_section7(d7_obj, request)
		return show_section7(request, True)	
	else:
		return show_section7(request, False)		

@login_required(login_url='core:login')
def show_section7(request, is_save):
	form = DInfant.objects.get(id=request.session['form_id'])
	participant = Participant.objects.get(id=request.session['participant_id'])
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all	
	date_interviewed = form.date_interviewed.strftime('%Y-%m-%d')
	date_data_entered = form.date_data_entered.strftime('%Y-%m-%d')
	date_admission = form.date_admission.strftime('%Y-%m-%d')
	role = ''
	if not request.user.is_staff:
		role = 'staff'
	try:
		d7_obj = D7Infection.objects.get(d_form_id=form.id) 
		#dob = d7_obj.a1m_dob.strftime('%Y-%m-%d')
		#moving_date = d7_obj.a1m_moving_date.strftime('%Y-%m-%d')
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				return render(request, 'forms/section7.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d7_obj})
			else:
				return render(request, 'forms/section7.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d7_obj})
		else:
			if is_save:	
				return render(request, 'forms/section7.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d7_obj})
			else:
				return render(request, 'forms/section7.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d7_obj})	
	except:
		return render(request, 'forms/section7.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section7(d7_obj, request):
	return None

###### CONTROLLER SECTION8
@login_required(login_url='core:login')
def process_section8(request):
	if request.POST.get('form_id'):
		request.session['form_id'] = request.POST.get('form_id')
	d_form_obj = DInfant.objects.get(id=int(request.session['form_id']))
	try:
		d8_obj = D8PollutantExposure.objects.get(d_form=d_form_obj)
		return update_section8(request)	
	except:
		return create_section8(request)

@login_required(login_url='core:login')
def create_section8(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d_form_obj = DInfant.objects.get(id=request.session['form_id'])
		d8_obj = D8PollutantExposure()
		d8_obj.d_form = d_form_obj
		d8_obj = save_section8(d8_obj, request)
		return show_section8(request, True)	
	else:
		return show_section8(request, False)
		
@login_required(login_url='core:login')
def update_section8(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		d8_obj = D8PollutantExposure.objects.get(d_form_id=request.session['form_id'])
		d8_obj = save_section8(d8_obj, request)
		return show_section8(request, True)	
	else:
		return show_section8(request, False)		

@login_required(login_url='core:login')
def show_section8(request, is_save):
	form = DInfant.objects.get(id=request.session['form_id'])
	participant = Participant.objects.get(id=request.session['participant_id'])
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all	
	date_interviewed = form.date_interviewed.strftime('%Y-%m-%d')
	date_data_entered = form.date_data_entered.strftime('%Y-%m-%d')
	date_admission = form.date_admission.strftime('%Y-%m-%d')
	role = ''
	if not request.user.is_staff:
		role = 'staff'
	try:
		d8_obj = D8PollutantExposure.objects.get(d_form_id=form.id) 
		#dob = d8_obj.a1m_dob.strftime('%Y-%m-%d')
		#moving_date = d8_obj.a1m_moving_date.strftime('%Y-%m-%d')
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				return render(request, 'forms/section8.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d8_obj})
			else:
				return render(request, 'forms/section8.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d8_obj})
		else:
			if is_save:	
				return render(request, 'forms/section8.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d8_obj})
			else:
				return render(request, 'forms/section8.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : d8_obj})	
	except:
		return render(request, 'forms/section8.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section8(d8_obj, request):
	d8_obj.d8m_charcoal = request.POST.get('d8m_charcoal')
	d8_obj.d8m_kerosene = request.POST.get('d8m_kerosene')
	d8_obj.d8m_wood = request.POST.get('d8m_wood')
	d8_obj.d8m_gas = request.POST.get('d8m_gas')
	d8_obj.d8m_electric = request.POST.get('d8m_electric')
	d8_obj.d8m_other = request.POST.get('d8m_other')
	d8_obj.d8m_cooking_exhaust = request.POST.get('d8m_cooking_exhaust')
	d8_obj.d8m_pesticide = request.POST.get('d8m_pesticide')	
	
	d8_obj.d8m_garbage_burning = request.POST.get('d8m_garbage_burning')
	d8_obj.d8m_pet = request.POST.get('d8m_pet')

	d8_obj.d8m_housing_type = request.POST.get('d8m_housing_type')
	
	d8_obj.d8m_landed_house_type = request.POST.get('d8m_landed_house_type')
	d8_obj.d8m_dampness_house = request.POST.get('d8m_dampness_house')
	d8_obj.d8m_ac = request.POST.get('d8m_ac')
	d8_obj.d8m_fan = request.POST.get('d8m_fan')
	d8_obj.d8m_air_filter = request.POST.get('d8m_air_filter')
	d8_obj.d8m_staying_out_history = request.POST.get('d8m_staying_out_history')
	##
	d8_obj.d8m_staying_out_1st_street = request.POST.get('d8m_staying_out_1st_street')
	d8_obj.d8m_staying_out_1st_rt = request.POST.get('d8m_staying_out_1st_rt')
	d8_obj.d8m_staying_out_1st_rw = request.POST.get('d8m_staying_out_1st_rw')
	d8_obj.d8m_staying_out_1st_district = request.POST.get('d8m_staying_out_1st_district')
	d8_obj.d8m_staying_out_1st_city = request.POST.get('d8m_staying_out_1st_city')
	d8_obj.d8m_staying_out_1st_zipcode = request.POST.get('d8m_staying_out_1st_zipcode')
	d8_obj.d8m_staying_out_1st_duration = request.POST.get('d8m_staying_out_1st_duration')

	d8_obj.d8m_staying_out_2nd_street = request.POST.get('d8m_staying_out_2nd_street')
	d8_obj.d8m_staying_out_2nd_rt = request.POST.get('d8m_staying_out_2nd_rt')
	d8_obj.d8m_staying_out_2nd_rw = request.POST.get('d8m_staying_out_2nd_rw')
	d8_obj.d8m_staying_out_2nd_district = request.POST.get('d8m_staying_out_2nd_district ')
	d8_obj.d8m_staying_out_2nd_city = request.POST.get('d8m_staying_out_2nd_city')
	d8_obj.d8m_staying_out_2nd_zipcode = request.POST.get('d8m_staying_out_2nd_zipcode')
	d8_obj.d8m_staying_out_2nd_duration = request.POST.get('d8m_staying_out_2nd_duration')

	if request.user.is_staff:
		d8_obj.d_form.is_save_all = True
		d8_obj.d_form.save()
	return d8_obj