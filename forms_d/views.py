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
		participant_id = request.session['participant_id']
		child_id = 1
		d_obj = DInfant()
		d_obj.participant_id = participant_id
		d_obj.child_id = child_id	#sesuikan lagi child id nya agar bisa milih dari tabel infant
		d_obj.interviewer_id = request.POST.get('interviewer_id')
		d_obj.data_entry_id = request.user.username
		number_of_visit = DInfant.objects.filter(participant_id=participant_id, child_id=child_id).count()
		d_obj.number_child_visit = (number_of_visit+1)
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
		return render(request, 'forms_d/form.html', {'staff_list' : staff_list, 'context' : 'create_new_form', 'participant' : participant, 'date_admission' : date_admission})

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
		#dob = d1_obj.d1m_dob.strftime('%Y-%m-%d')
		#moving_date = d1_obj.d1m_moving_date.strftime('%Y-%m-%d')
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				return render(request, 'forms_d/section1.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd1' : d1_obj})
			else:
				return render(request, 'forms_d/section1.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd1' : d1_obj})
		else:
			if is_save:	
				return render(request, 'forms_d/section1.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd1' : d1_obj})
			else:
				return render(request, 'forms_d/section1.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd1' : d1_obj})	
	except:
		return render(request, 'forms_d/section1.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

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

	if request.POST.get('d1c_vaccination_history') == "1":
		d1_obj.d1c_vaccination_history = True
	else:
		d1_obj.d1c_vaccination_history = False	

	if request.POST.get('d1c_bcg') == "on":
		d1_obj.d1c_bcg = True
		d1_obj.d1c_bcg_date = request.POST.get('d1c_bcg_date')
	else:
		d1_obj.d1c_bcg = False
		d1_obj.d1c_bcg_date = None
		
	if request.POST.get('d1c_hep_b') == "on":
		d1_obj.d1c_hep_b = True
		d1_obj.d1c_hep_b_date = request.POST.get('d1c_hep_b_date')
	else:
		d1_obj.d1c_hep_b = False
		d1_obj.d1c_hep_b_date = None	
				
	if request.POST.get('d1c_dpt') == "on":
		d1_obj.d1c_dpt = True
		d1_obj.d1c_dpt_date = request.POST.get('d1c_dpt_date')
	else:
		d1_obj.d1c_dpt = False
		d1_obj.d1c_dpt_date = None	
				
	if request.POST.get('d1c_ipv') == "on":
		d1_obj.d1c_ipv = True
		d1_obj.d1c_ipv_date = request.POST.get('d1c_ipv_date')
	else:
		d1_obj.d1c_ipv = False
		d1_obj.d1c_ipv_date = None
				
	if request.POST.get('d1c_opv') == "on":
		d1_obj.d1c_opv = True
		d1_obj.d1c_opv_date = request.POST.get('d1c_opv_date')
	else:
		d1_obj.d1c_opv = False
		d1_obj.d1c_opv_date = None
			
	if request.POST.get('d1c_hib') == "on":
		d1_obj.d1c_hib = True
		d1_obj.d1c_hib_date = request.POST.get('d1c_hib_date')
	else:
		d1_obj.d1c_hib = False
		d1_obj.d1c_hib_date = None
				
	if request.POST.get('d1c_rotavirus') == "on":
		d1_obj.d1c_rotavirus = True
		d1_obj.d1c_rotavirus_date = request.POST.get('d1c_rotavirus_date')
	else:
		d1_obj.d1c_rotavirus = False
		d1_obj.d1c_rotavirus_date = None	
			
	if request.POST.get('d1c_pneumococcus') == "on":
		d1_obj.d1c_pneumococcus = True
		d1_obj.d1c_pneumococcus_date = request.POST.get('d1c_pneumococcus_date')
	else:
		d1_obj.d1c_pneumococcus = False
		d1_obj.d1c_pneumococcus_date = None

	if request.POST.get('d1c_influenza') == "on":
		d1_obj.d1c_influenza = True
		d1_obj.d1c_influenza_date = request.POST.get('d1c_influenza_date')
	else:
		d1_obj.d1c_influenza = False
		d1_obj.d1c_influenza_date = None

	d1_obj.save()
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
				return render(request, 'forms_d/section2.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd2' : d2_obj})
			else:
				return render(request, 'forms_d/section2.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd2' : d2_obj})
		else:
			if is_save:	
				return render(request, 'forms_d/section2.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd2' : d2_obj})
			else:
				return render(request, 'forms_d/section2.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd2' : d2_obj})	
	except:
		return render(request, 'forms_d/section2.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section2(d2_obj, request):
	if request.POST.get('d2c_breast_feeding_status') == "1":
		d2_obj.d2c_breast_feeding_status = True
		d2_obj.d2c_supplementary_food = False
	else:
		d2_obj.d2c_breast_feeding_status = False	
		d2_obj.d2c_supplementary_food = True


	if request.POST.get('d2c_infant_formula') == "on":		
		d2_obj.d2c_infant_formula = True
		d2_obj.d2c_age_formula = request.POST.get('d2c_age_formula')	
	else:
		d2_obj.d2c_infant_formula = False
		d2_obj.d2c_age_formula = None				
	

	if request.POST.get('d2c_cows_milk_formula') == "on":
		d2_obj.d2c_cows_milk_formula = True
	else:
		d2_obj.d2c_cows_milk_formula = False
				
	if request.POST.get('d2c_soy_formula') == "on":	
		d2_obj.d2c_soy_formula = True
	else:
		d2_obj.d2c_soy_formula = False

	if request.POST.get('d2c_hypo_allergen_formula') == "on":
		d2_obj.d2c_hypo_allergen_formula = True
	else:
		d2_obj.d2c_hypo_allergen_formula = False

	if request.POST.get('d2c_hydrolized_formula') == "on":
		d2_obj.d2c_hydrolized_formula = True
	else:
		d2_obj.d2c_hydrolized_formula = False
	if request.POST.get('d2c_amino_formula') == "on":
		d2_obj.d2c_amino_formula = True
	else:
		d2_obj.d2c_amino_formula = False	

	if request.POST.get('d2c_weaning_food') == "on":	
		d2_obj.d2c_weaning_food = True
		d2_obj.d2c_age_weaning_food = request.POST.get('d2c_age_weaning_food')
	else:
		d2_obj.d2c_weaning_food = False
		d2_obj.d2c_age_weaning_food = None
		
		
	d2_obj.save()
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
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				return render(request, 'forms_d/section3.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd3' : d3_obj})
			else:
				return render(request, 'forms_d/section3.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd3' : d3_obj})
		else:
			if is_save:	
				return render(request, 'forms_d/section3.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd3' : d3_obj})
			else:
				return render(request, 'forms_d/section3.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd3' : d3_obj})	
	except:
		return render(request, 'forms_d/section3.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

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
	
	if request.POST.get('d3c_heart_abnormality') == "1":
		d3_obj.d3c_heart_abnormality = True
		d3_obj.d3c_heart_abnormality_detail = request.POST.get('d3c_heart_abnormality_detail')
	else:
		d3_obj.d3c_heart_abnormality = False
		d3_obj.d3c_heart_abnormality_detail = ""
			
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
	
	if request.POST.get('d3c_cineloops_abdominal') == "1":
		d3_obj.d3c_cineloops_abdominal = True
	else:
		d3_obj.d3c_cineloops_abdominal = False	

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
	d3_obj.save()
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
				return render(request, 'forms_d/section4.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd4' : d4_obj})
			else:
				return render(request, 'forms_d/section4.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd4' : d4_obj})
		else:
			if is_save:	
				return render(request, 'forms_d/section4.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd4' : d4_obj})
			else:
				return render(request, 'forms_d/section4.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd4' : d4_obj})	
	except:
		return render(request, 'forms_d/section4.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section4(d4_obj, request):
	d4_obj.d4c_date_lung = request.POST.get('d4c_date_lung')
	d4_obj.d4c_examiner_lung = request.POST.get('d4c_examiner_lung')
	d4_obj.d4c_resistance_1st = request.POST.get('d4c_resistance_1st')
	d4_obj.d4c_resistance_2nd = request.POST.get('d4c_resistance_2nd')
	d4_obj.d4c_compliance_1st = request.POST.get('d4c_compliance_1st')
	d4_obj.d4c_compliance_2nd = request.POST.get('d4c_compliance_2nd')
	d4_obj.d4c_time_constant_1st = request.POST.get('d4c_time_constant_1st')
	d4_obj.d4c_time_constant_2nd = request.POST.get('d4c_time_constant_2nd')
	d4_obj.d4c_fvc_1st = request.POST.get('d4c_fvc_1st')
	d4_obj.d4c_fvc_2nd = request.POST.get('d4c_fvc_2nd')
	d4_obj.d4c_fev_1st = request.POST.get('d4c_fev_1st')
	d4_obj.d4c_fev_2nd = request.POST.get('d4c_fev_2nd')
	
	if request.POST.get('d4c_respiratory_symptom') == "1":
		d4_obj.d4c_respiratory_symptom = True
	else:
		d4_obj.d4c_respiratory_symptom = False
	
	if request.POST.get('d4c_dry_cough'):	
		d4_obj.d4c_dry_cough = request.POST.get('d4c_dry_cough')
		print "ok oce"
	else:
		d4_obj.d4c_dry_cough = ""

	if request.POST.get('d4c_phlegmy_cough'): 	
		d4_obj.d4c_phlegmy_cough = request.POST.get('d4c_phlegmy_cough')
	else:
		d4_obj.d4c_phlegmy_cough = ""

	if request.POST.get('d4c_runny_nose'):	
		d4_obj.d4c_runny_nose = request.POST.get('d4c_runny_nose')
	else:
		d4_obj.d4c_runny_nose = ""

	if request.POST.get('d4c_stuffed_nose'):	
		d4_obj.d4c_stuffed_nose = request.POST.get('d4c_stuffed_nose')
	else:
		d4_obj.d4c_stuffed_nose = ""

	if request.POST.get('d4c_wheeze'):
		d4_obj.d4c_wheeze = request.POST.get('d4c_wheeze')
	else:
		d4_obj.d4c_wheeze = ""

	if request.POST.get('d4c_breath_shortness'):	
		d4_obj.d4c_breath_shortness = request.POST.get('d4c_breath_shortness')
	else:
		d4_obj.d4c_breath_shortness = ""

	if request.POST.get('d4c_rattly_chest'):	
		d4_obj.d4c_rattly_chest = request.POST.get('d4c_rattly_chest')
	else:
		d4_obj.d4c_rattly_chest = ""
	
	if request.POST.get('d4c_snoring'): 	
		d4_obj.d4c_snoring = request.POST.get('d4c_snoring')
	else:
		d4_obj.d4c_snoring = ""
	
	if request.POST.get('d4c_stridor'):	
		d4_obj.d4c_stridor = request.POST.get('d4c_stridor')
	else:
		d4_obj.d4c_stridor = ""

	d4_obj.save()
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
				return render(request, 'forms_d/section5.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd5' : d5_obj})
			else:
				return render(request, 'forms_d/section5.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd5' : d5_obj})
		else:
			if is_save:	
				return render(request, 'forms_d/section5.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd5' : d5_obj})
			else:
				return render(request, 'forms_d/section5.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd5' : d5_obj})	
	except:
		return render(request, 'forms_d/section5.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section5(d5_obj, request):
	if request.POST.get('d5c_blood') == "on":
		d5_obj.d5c_blood = True
		d5_obj.d5c_blood_date = request.POST.get('d5c_blood_date')
	else:
		d5_obj.d5c_blood = False	
		d5_obj.d5c_blood_date = None
	
	if request.POST.get('d5c_buccal_swab') == "on":
		d5_obj.d5c_buccal_swab = True
		d5_obj.d5c_buccal_swab_date = request.POST.get('d5c_buccal_swab_date')
	else:
		d5_obj.d5c_buccal_swab = False
		d5_obj.d5c_buccal_swab_date = None
	
	if request.POST.get('d5c_hair_1') == "on":
		d5_obj.d5c_hair_1 = True
		d5_obj.d5c_hair_1_date = request.POST.get('d5c_hair_1_date')
	else:
		d5_obj.d5c_hair_1 = False
		d5_obj.d5c_hair_1_date = None

	if request.POST.get('d5c_hair_6') == "on":
		d5_obj.d5c_hair_6 = True
		d5_obj.d5c_hair_6_date = request.POST.get('d5c_hair_6_date')
	else:
		d5_obj.d5c_hair_6 = False
		d5_obj.d5c_hair_6_date = None

	if request.POST.get('d5c_nail_1') == "on":
		d5_obj.d5c_nail_1 = True
		d5_obj.d5c_nail_1_date = request.POST.get('d5c_nail_1_date')
	else:
		d5_obj.d5c_nail_1 = False
		d5_obj.d5c_nail_1_date = None

	if request.POST.get('d5c_nail_6') == "on":
		d5_obj.d5c_nail_6 = True
		d5_obj.d5c_nail_6_date = request.POST.get('d5c_nail_6_date')
	else:
		d5_obj.d5c_nail_6 = False
		d5_obj.d5c_nail_6_date = None

	if request.POST.get('d5c_nasopharyngeal_2') == "on":
		d5_obj.d5c_nasopharyngeal_2 = True
		d5_obj.d5c_nasopharyngeal_2_date = request.POST.get('d5c_nasopharyngeal_2_date')
	else:
		d5_obj.d5c_nasopharyngeal_2 = False
		d5_obj.d5c_nasopharyngeal_2_date = None

	if request.POST.get('d5c_nasopharyngeal_4') == "on":
		d5_obj.d5c_nasopharyngeal_4 = True
		d5_obj.d5c_nasopharyngeal_4_date = request.POST.get('d5c_nasopharyngeal_4_date')
	else:
		d5_obj.d5c_nasopharyngeal_4 = False
		d5_obj.d5c_nasopharyngeal_4_date = None

	if request.POST.get('d5c_nasopharyngeal_6') == "on":
		d5_obj.d5c_nasopharyngeal_6 = True
		d5_obj.d5c_nasopharyngeal_6_date = request.POST.get('d5c_nasopharyngeal_6_date')
	else:
		d5_obj.d5c_nasopharyngeal_6 = False
		d5_obj.d5c_nasopharyngeal_6_date = None

	d5_obj.save()
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
				return render(request, 'forms_d/section6.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd6' : d6_obj})
			else:
				return render(request, 'forms_d/section6.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd6' : d6_obj})
		else:
			if is_save:	
				return render(request, 'forms_d/section6.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd6' : d6_obj})
			else:
				return render(request, 'forms_d/section6.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd6' : d6_obj})	
	except:
		return render(request, 'forms_d/section6.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section6(d6_obj, request):
	d6_obj.d6m_smoking_status = request.POST.get('d6m_smoking_status')
	if request.POST.get('d6m_quitting_smoke') == "1":
		d6_obj.d6m_quitting_smoke = True
		d6_obj.d6m_quitting_duration = request.POST.get('d6m_quitting_duration')
	else:
		d6_obj.d6m_quitting_smoke = False
		d6_obj.d6m_quitting_duration = None

	if request.POST.get('d6m_cigar_number'):
		d6_obj.d6m_cigar_number = request.POST.get('d6m_cigar_number')
	else:
		d6_obj.d6m_cigar_number = None

	if request.POST.get('d6m_cigar_type') == "1":
		d6_obj.d6m_cigar_type = True
	else:
		d6_obj.d6m_cigar_type = False

		
	if request.POST.get('d6m_smoking_household') == "1":
		d6_obj.d6m_smoking_household = True
	else:
		d6_obj.d6m_smoking_household = False	
	
	if request.POST.get('d6m_household_number'):
		d6_obj.d6m_household_number = request.POST.get('d6m_household_number')
	else:
		d6_obj.d6m_household_number = None

	if request.POST.get('d6m_household_cigar_number'):
		d6_obj.d6m_household_cigar_number = request.POST.get('d6m_household_cigar_number')
	else:
		d6_obj.d6m_household_cigar_number = None	
	
	if request.POST.get('d6m_household_presence') == "1":
		d6_obj.d6m_household_presence = True
	else:
		d6_obj.d6m_household_presence = False
	

	d6_obj.d6f_smoking_status = request.POST.get('d6f_smoking_status')

	if request.POST.get('d6f_quitting_duration'):	
		d6_obj.d6f_quitting_duration = request.POST.get('d6f_quitting_duration')
	else:
		d6_obj.d6f_quitting_duration = None

	if request.POST.get('d6f_cigar_number'):	
		d6_obj.d6f_cigar_number = request.POST.get('d6f_cigar_number')
	else:
		d6_obj.d6f_cigar_number = None

	if request.POST.get('d6f_cigar_type') == "1":
		d6_obj.d6f_cigar_type = True
	else:
		d6_obj.d6f_cigar_type = False
	
	if request.POST.get('d6f_smoking_frequency'):	
		d6_obj.d6f_smoking_frequency = request.POST.get('d6f_smoking_frequency')
	else:
		d6_obj.d6f_smoking_frequency = ""

	if request.POST.get('d6f_smoking_presence') == "1":
		d6_obj.d6f_smoking_presence = True
	else:
		d6_obj.d6f_smoking_presence = False	
	
	d6_obj.save()
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
				return render(request, 'forms_d/section7.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd7' : d7_obj})
			else:
				return render(request, 'forms_d/section7.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd7' : d7_obj})
		else:
			if is_save:	
				return render(request, 'forms_d/section7.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd7' : d7_obj})
			else:
				return render(request, 'forms_d/section7.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd7' : d7_obj})	
	except:
		return render(request, 'forms_d/section7.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section7(d7_obj, request): 
	if request.POST.get('d7c_infection') == "1":
		d7_obj.d7c_infection = True
	else:
		d7_obj.d7c_infection = False
	
	if request.POST.get('d7c_infection_upper_respi') == "on":	
		d7_obj.d7c_infection_upper_respi = True
	else:
		d7_obj.d7c_infection_upper_respi = False	
	
	if request.POST.get('d7c_infection_lower_respi') == "on":
		d7_obj.d7c_infection_lower_respi = True
	else:
		d7_obj.d7c_infection_lower_respi = False
	
	if request.POST.get('d7c_infection_gastro') == "on":		
		d7_obj.d7c_infection_gastro = True
	else:
		d7_obj.d7c_infection_gastro = False
	
	if request.POST.get('d7c_infection_urinary') == "on":		
		d7_obj.d7c_infection_urinary = True
	else:
		d7_obj.d7c_infection_urinary = False
	
	if request.POST.get('d7c_infection_cns') == "on":		
		d7_obj.d7c_infection_cns = True
	else:
		d7_obj.d7c_infection_cns = False
	
	if 	request.POST.get('d7c_infection_sepsis') == "on":
		d7_obj.d7c_infection_sepsis = True
	else:
		d7_obj.d7c_infection_sepsis = False
	
	if request.POST.get('d7c_infection_dengue') == "on":
		d7_obj.d7c_infection_dengue = True
	else:
		d7_obj.d7c_infection_dengue = False		 	
	
	if request.POST.get('d7c_infection_others') == "on":
		d7_obj.d7c_infection_others = True
	else:
		d7_obj.d7c_infection_others = False
	d7_obj.d7c_infection_others_detail = request.POST.get('d7c_infection_others_detail')	
	
	if request.POST.get('d7c_infection_unknown') == "on":		
		d7_obj.d7c_infection_unknown = True
	else:
		d7_obj.d7c_infection_unknown = False
	d7_obj.d7c_physician_clinic = request.POST.get('d7c_physician_clinic')
	d7_obj.d7c_contact = request.POST.get('d7c_contact')

	if request.POST.get('d7c_infection_symptoms') == "on":
		d7_obj.d7c_infection_symptoms = True
	else:
		d7_obj.d7c_infection_symptoms = False

	if request.POST.get('d7c_symptoms_respi') == "on":
		d7_obj.d7c_symptoms_respi = True
	else:
		d7_obj.d7c_symptoms_respi = False

	if request.POST.get('d7c_symptoms_gastro') == "on":	
		d7_obj.d7c_symptoms_gastro = True
	else:
		d7_obj.d7c_symptoms_gastro = False

	if request.POST.get('d7c_symptoms_skin') == "on":	
		d7_obj.d7c_symptoms_skin = True
	else:
		d7_obj.d7c_symptoms_skin = False

	if request.POST.get('d7c_symptoms_nervous') == "on":		
		d7_obj.d7c_symptoms_nervous = True
	else:
		d7_obj.d7c_symptoms_nervous = False

	print "hospitalization" + request.POST.get('d7c_hospitalization')	
	if request.POST.get('d7c_hospitalization') == "1":		
		d7_obj.d7c_hospitalization = True
		d7_obj.d7c_admission_date = request.POST.get('d7c_admission_date')
		d7_obj.d7c_discharged_date = request.POST.get('d7c_discharged_date')
	else:
		d7_obj.d7c_hospitalization = False
		d7_obj.d7c_admission_date = None
		d7_obj.d7c_discharged_date = None
	
	d7_obj.d7c_hospital = request.POST.get('d7c_hospital')
	d7_obj.d7c_physician = request.POST.get('d7c_physician')
	d7_obj.d7c_hospital_contact = request.POST.get('d7c_hospital_contact')
		
	print "ward "+request.POST.get('d7c_ward')	
	if request.POST.get('d7c_ward'):
		d7_obj.d7c_ward = request.POST.get('d7c_ward')
	else:
		d7_obj.d7c_ward = ""	
		
	if request.POST.get('d7c_additional_test') == "on":
		d7_obj.d7c_additional_test = True
	else:
		d7_obj.d7c_additional_test = False

	if request.POST.get('d7c_blood_test') == "on":		
		d7_obj.d7c_blood_test = True
	else:
		d7_obj.d7c_blood_test = False

	if request.POST.get('d7c_blood_count') == "on":		
		d7_obj.d7c_blood_count = True
	else:
		d7_obj.d7c_blood_count = False

	if request.POST.get('d7c_crp') == "on":		
		d7_obj.d7c_crp = True
	else:
		d7_obj.d7c_crp = False	

	if request.POST.get('d7c_procalcitonin') == "on":	
		d7_obj.d7c_procalcitonin = True
	else:
		d7_obj.d7c_procalcitonin = False

	if request.POST.get('d7c_blood_culture') == "on":		
		d7_obj.d7c_blood_culture = True
		d7_obj.d7c_blood_culture_date = request.POST.get('d7c_blood_culture_date')
	else:
		d7_obj.d7c_blood_culture = False
		d7_obj.d7c_blood_culture_date = None

	d7_obj.d7c_blood_microorganism = request.POST.get('d7c_blood_microorganism')

	if request.POST.get('d7c_typhoid') == "on":
		d7_obj.d7c_typhoid = True
	else:
		d7_obj.d7c_typhoid = False

	if request.POST.get('d7c_dengue_ns_1') == "on":		
		d7_obj.d7c_dengue_ns_1 = True
	else:
		d7_obj.d7c_dengue_ns_1 = False

	if request.POST.get('d7c_dengue') == "on":		
		d7_obj.d7c_dengue = True
	else:
		d7_obj.d7c_dengue = False

	if request.POST.get('d7c_nasopharyngeal') == "on":		
		d7_obj.d7c_nasopharyngeal = True
	else:
		d7_obj.d7c_nasopharyngeal = False

	if request.POST.get('d7c_urine') == "on":		
		d7_obj.d7c_urine = True
	else:
		d7_obj.d7c_urine = False

	if request.POST.get('d7c_urinalysis ') == "on": 		
		d7_obj.d7c_urinalysis = True
		d7_obj.d7c_urinalysis_date = request.POST.get('d7c_urinalysis_date')
	else:
		d7_obj.d7c_urinalysis = False		
		d7_obj.d7c_urinalysis_date = None
	
	if request.POST.get('d7c_urine_culture') == "on": 
		d7_obj.d7c_urine_culture = True
		d7_obj.d7c_urine_date = request.POST.get('d7c_urine_date')
	else:
		d7_obj.d7c_urine_culture = False		
		d7_obj.d7c_urine_date = None

	d7_obj.d7c_urine_microorganism = request.POST.get('d7c_urine_microorganism')
	
	if request.POST.get('d7c_csf') == "on":
		d7_obj.d7c_csf = True
		d7_obj.d7c_csf_date = request.POST.get('d7c_csf_date')
	else:
		d7_obj.d7c_csf = False	
		d7_obj.d7c_csf_date = None

	d7_obj.d7c_csf_microorganism = request.POST.get('d7c_csf_microorganism')
	
	if request.POST.get('d7c_faecal_culture') == "on":
		d7_obj.d7c_faecal_culture = True
		d7_obj.d7c_faecal_date = request.POST.get('d7c_faecal_date')
	else:
		d7_obj.d7c_faecal_culture = False		
		d7_obj.d7c_faecal_date = None

	d7_obj.d7c_faecal_microorganism = request.POST.get('d7c_faecal_microorganism')
	
	if request.POST.get('d7c_chest_xray') == "on":
		d7_obj.d7c_chest_xray = True
	else:
		d7_obj.d7c_chest_xray = False	
	d7_obj.d7c_chest_xray_findings = request.POST.get('d7c_chest_xray_findings')
	
	if request.POST.get('d7c_usg') == "on":
		d7_obj.d7c_usg = True
		d7_obj.d7c_usg_date = None
	else:
		d7_obj.d7c_usg = False
		d7_obj.d7c_usg_date = None

	d7_obj.d7c_usg_type = request.POST.get('d7c_usg_type')
	d7_obj.d7c_usg_findings = request.POST.get('d7c_usg_findings')
	
	if request.POST.get('d7c_mri') == "on":
		d7_obj.d7c_mri = True
		d7_obj.d7c_mri_date = request.POST.get('d7c_mri_date')
	else:
		d7_obj.d7c_mri = False	
		d7_obj.d7c_mri_date = None

	d7_obj.d7c_mri_type = request.POST.get('d7c_mri_type')
	
	d7_obj.d7c_mri_findings = request.POST.get('d7c_mri_findings')
	
	if request.POST.get('d7c_other_test') == "on":
		d7_obj.d7c_other_test = True
		d7_obj.d7c_other_test_date = request.POST.get('d7c_other_test_date')
	else:
		d7_obj.d7c_other_test = False
		d7_obj.d7c_other_test_date = None	
	d7_obj.d7c_other_test_type = request.POST.get('d7c_other_test_type')
	
	d7_obj.d7c_other_test_findings = request.POST.get('d7c_other_test_findings')
	
	if request.POST.get('d7c_medication') == "1":
		d7_obj.d7c_medication = True
	else:
		d7_obj.d7c_medication = False

	d7_obj.d7c_med1_name = request.POST.get('d7c_med1_name')
	d7_obj.d7c_med1_dosage = request.POST.get('d7c_med1_dosage')
	if request.POST.get('d7c_med1_name'):
		d7_obj.d7c_med1_start_date = request.POST.get('d7c_med1_start_date')
		d7_obj.d7c_med1_end_date = request.POST.get('d7c_med1_end_date')
	else:
		d7_obj.d7c_med1_start_date = None
		d7_obj.d7c_med1_end_date = None

	d7_obj.d7c_med2_name = request.POST.get('d7c_med2_name')
	d7_obj.d7c_med2_dosage = request.POST.get('d7c_med2_dosage')
	if request.POST.get('d7c_med2_name'):
		d7_obj.d7c_med2_start_date = request.POST.get('d7c_med2_start_date')
		d7_obj.d7c_med2_end_date = request.POST.get('d7c_med2_end_date')
	else:
		d7_obj.d7c_med2_start_date = None
		d7_obj.d7c_med2_end_date = None

	d7_obj.d7c_med3_name = request.POST.get('d7c_med3_name')
	d7_obj.d7c_med3_dosage = request.POST.get('d7c_med3_dosage')
	if request.POST.get('d7c_med3_name'):
		d7_obj.d7c_med3_start_date = request.POST.get('d7c_med3_start_date')
		d7_obj.d7c_med3_end_date = request.POST.get('d7c_med3_end_date')
	else:
		d7_obj.d7c_med3_start_date = None
		d7_obj.d7c_med3_end_date = None

	d7_obj.d7c_med4_name = request.POST.get('d7c_med4_name')
	d7_obj.d7c_med4_dosage = request.POST.get('d7c_med4_dosage')
	if request.POST.get('d7c_med4_name'):
		d7_obj.d7c_med4_start_date = request.POST.get('d7c_med4_start_date')
		d7_obj.d7c_med4_end_date = request.POST.get('d7c_med4_end_date')
	else:
		d7_obj.d7c_med4_start_date = None
		d7_obj.d7c_med4_end_date = None

	d7_obj.d7c_med5_name = request.POST.get('d7c_med5_name')
	d7_obj.d7c_med5_dosage = request.POST.get('d7c_med5_dosage')
	if request.POST.get('d7c_med5_name'):
		d7_obj.d7c_med5_start_date = request.POST.get('d7c_med5_start_date')
		d7_obj.d7c_med5_end_date = request.POST.get('d7c_med5_end_date')
	else:
		d7_obj.d7c_med5_start_date = None
		d7_obj.d7c_med5_end_date = None

	d7_obj.save()
	if request.user.is_staff:
		d7_obj.d_form.is_save_all = True
		d7_obj.d_form.save()
	return d7_obj

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
				return render(request, 'forms_d/section8.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd8' : d8_obj})
			else:
				return render(request, 'forms_d/section8.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd8' : d8_obj})
		else:
			if is_save:	
				return render(request, 'forms_d/section8.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd8' : d8_obj})
			else:
				return render(request, 'forms_d/section8.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'd8' : d8_obj})	
	except:
		return render(request, 'forms_d/section8.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section8(d8_obj, request):
	if request.POST.get('d8m_charcoal') == "on":
		d8_obj.d8m_charcoal = True
	else:
		d8_obj.d8m_charcoal = False
	if request.POST.get('d8m_kerosene') == "on":
		d8_obj.d8m_kerosene = True
	else:
		d8_obj.d8m_kerosene = False
	if request.POST.get('d8m_wood') == "on":	
		d8_obj.d8m_wood = True
	else:
		d8_obj.d8m_wood = False
	if request.POST.get('d8m_gas') == "on":
		d8_obj.d8m_gas = True
	else:
		d8_obj.d8m_gas = False
	
	if request.POST.get('d8m_electric') == "on":			
		d8_obj.d8m_electric = True
	else:
		d8_obj.d8m_electric = False

	if request.POST.get('d8m_other') == "on":		
		d8_obj.d8m_other = True
	else:
		d8_obj.d8m_other = False
	d8_obj.d8m_other_detail = request.POST.get('d8m_other_detail')
			
	if request.POST.get('d8m_cooking_exhaust') == "1":
		d8_obj.d8m_cooking_exhaust = True
	else:
		d8_obj.d8m_cooking_exhaust = False
	
	if request.POST.get('d8m_pesticide') == "1":			
		d8_obj.d8m_pesticide = 	True
	else:
		d8_obj.d8m_pesticide = 	False	
	
	d8_obj.d8m_garbage_burning = request.POST.get('d8m_garbage_burning')
	
	if request.POST.get('d8m_pet') == "1":
		d8_obj.d8m_pet = True
	else:
		d8_obj.d8m_pet = False	
	
	d8_obj.d8m_housing_type = request.POST.get('d8m_housing_type')
	print d8_obj.d8m_housing_type
	if request.POST.get('d8m_housing_type') == "1":
		d8_obj.d8m_landed_house_type = request.POST.get('d8m_landed_house_type')
		d8_obj.d8m_apartment_level_number = None
	else:
		d8_obj.d8m_apartment_level_number = request.POST.get('d8m_apartment_level_number')
		d8_obj.d8m_landed_house_type = ""
	
	if request.POST.get('d8m_dampness_house'):
		d8_obj.d8m_dampness_house = True
	else:
		d8_obj.d8m_dampness_house = False

	if request.POST.get('d8m_ac') == "on":		
		d8_obj.d8m_ac = True
	else:
		d8_obj.d8m_ac = False

	if request.POST.get('d8m_fan') == "on":	
		d8_obj.d8m_fan = True
	else:
		d8_obj.d8m_fan = False

	if request.POST.get('d8m_air_filter') == "on": 		
		d8_obj.d8m_air_filter = True
	else:
		d8_obj.d8m_air_filter = False

	if request.POST.get('d8m_staying_out_history') == "1": 		
		d8_obj.d8m_staying_out_history = True
	else:
		d8_obj.d8m_staying_out_history = False	
	##

	if request.POST.get('d8m_staying_out_1st_street'):
		d8_obj.d8m_staying_out_1st_street = request.POST.get('d8m_staying_out_1st_street')
		d8_obj.d8m_staying_out_1st_rt = request.POST.get('d8m_staying_out_1st_rt')
		d8_obj.d8m_staying_out_1st_rw = request.POST.get('d8m_staying_out_1st_rw')
		d8_obj.d8m_staying_out_1st_district = request.POST.get('d8m_staying_out_1st_district')
		d8_obj.d8m_staying_out_1st_city = request.POST.get('d8m_staying_out_1st_city')
		d8_obj.d8m_staying_out_1st_zipcode = request.POST.get('d8m_staying_out_1st_zipcode')
		d8_obj.d8m_staying_out_1st_duration = request.POST.get('d8m_staying_out_1st_duration')

	if request.POST.get('d8m_staying_out_2nd_street'):
		d8_obj.d8m_staying_out_2nd_street = request.POST.get('d8m_staying_out_2nd_street')
		d8_obj.d8m_staying_out_2nd_rt = request.POST.get('d8m_staying_out_2nd_rt')
		d8_obj.d8m_staying_out_2nd_rw = request.POST.get('d8m_staying_out_2nd_rw')
		d8_obj.d8m_staying_out_2nd_district = request.POST.get('d8m_staying_out_2nd_district ')
		d8_obj.d8m_staying_out_2nd_city = request.POST.get('d8m_staying_out_2nd_city')
		d8_obj.d8m_staying_out_2nd_zipcode = request.POST.get('d8m_staying_out_2nd_zipcode')
		d8_obj.d8m_staying_out_2nd_duration = request.POST.get('d8m_staying_out_2nd_duration')
	d8_obj.save()
	if request.user.is_staff:
		d8_obj.d_form.is_save_all = True
		d8_obj.d_form.save()
	return d8_obj