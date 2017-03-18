from django.shortcuts import render, redirect
from django.http import HttpResponse
# from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
import datetime


@login_required(login_url='core:login')
def check_form(request):
	form = CBirth.objects.get(id=request.session['form_id'])
	form.data_checked_id = request.user.username
	form.date_data_checked = datetime.date.today()
	form.save()
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all 	
	date_interviewed = form.date_interviewed.strftime('%Y-%m-%d')
	date_data_entered = form.date_data_entered.strftime('%Y-%m-%d')
	date_admission = form.date_admission.strftime('%Y-%m-%d')
	date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
	role = ''
	success = True
	if not request.user.is_staff:
		role = 'staff'
	try:
		c1_obj = CMother.objects.get(c_form_id=request.session['form_id']) 
		blood_test_date = c1_obj.c1m_blood_test_date.strftime('%Y-%m-%d')
		return render(request, 'forms/sectionC1.html', {'date_data_checked' : date_data_checked, 'success' : success, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'c1' : c1_obj, 'blood_test_date' : blood_test_date})
	except:
		return render(request, 'forms/sectionC1.html', {'date_data_checked' : date_data_checked, 'success' : success, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def save_form(request):
	form = CBirth.objects.get(id=request.session['form_id'])
	form.is_save_all = True
	form.save()
	return show_sectionC1(request, request.session['form_id'])

@login_required(login_url='core:login')
def edit_form(request):
	form = CBirth.objects.get(id=request.session['form_id'])
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all 	
	date_interviewed = form.date_interviewed.strftime('%Y-%m-%d')
	date_data_entered = form.date_data_entered.strftime('%Y-%m-%d')
	date_admission = form.date_admission.strftime('%Y-%m-%d')
	role = ''
	if not request.user.is_staff:
		role = 'staff'
	section_number = request.POST.get('section_number')
	if section_number == 1:
		try:
			c1_obj = CMother.objects.get(c_form_id=request.session['form_id']) 
			blood_test_date = c1_objc1_obj.c1m_blood_test_date.strftime('%Y-%m-%d')
			swab_date = c1_objc1_obj.c1m_swab_date.strftime('%Y-%m-%d')
			if form.date_data_checked is not None:
				date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
				return render(request, 'forms/edit_sectionC1.html', {'date_data_checked' : date_data_checked,'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'c1' : c1_obj, 'blood_test_date' : blood_test_date, 'swab_date' : swab_date})
			else:	
				return render(request, 'forms/edit_sectionC1.html', {'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'c1' : c1_obj, 'blood_test_date' : blood_test_date, 'blood_test_date' : blood_test_date, 'swab_date' : swab_date})
		except:
				return render(request, 'forms/edit_sectionC1.html', {'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})
	else:
		return render(request, 'forms/edit_sectionC1.html', {'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})					

@login_required(login_url='core:login')
def create_form(request):
	if request.method == "POST":		
		c_obj = CBirth()
		c_obj.participant_id = request.session['participant_id']	
		c_obj.interviewer_id = request.POST.get('interviewer_id')
		c_obj.data_entry_id = request.user.username
		c_obj.date_admission = request.POST.get('date_admission')
		c_obj.date_interviewed = request.POST.get('date_interviewed')
		c_obj.date_data_entered = request.POST.get('date_data_entered')
		c_obj.save()
		request.session['form_id'] = c_obj.id
		return process_sectionC1(request)
	else:
		participant = Participant.objects.get(id=request.session['participant_id'])
		date_admission = participant.date_admission.strftime('%Y-%m-%d')
		staff_list = User.objects.filter(is_staff=False)
		return render(request, 'forms_c/form.html', {'staff_list' : staff_list, 'context' : 'create', 'participant' : participant, 'date_admission' : date_admission})




####CONTROLLER SECTION C1
@login_required(login_url='core:login')
def process_sectionC1(request):	 
	if request.POST.get('form_id'):	
		request.session['form_id'] = request.POST.get('form_id')
	c_form_obj = CBirth.objects.get(id=int(request.session['form_id']))
	print c_form_obj
	try:
		c1_obj = CMother.objects.get(c_form=c_form_obj)
		print "masuk ke update_sectionC1"		
		return update_sectionC1(request)		
	except:
		print "masuk ke create_sectionC1"				
		return create_sectionC1(request)

@login_required(login_url='core:login')
def create_sectionC1(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		c_form_obj = CBirth.objects.get(id=request.session['form_id'])
		c1_obj = CMother()
		c1_obj.c_form = c_form_obj
		c1_obj = save_sectionC1(c1_obj, request)
		print "masuk ke show_sectionC1 true"		
		return show_sectionC1(request, True)	
	else:		
		print "masuk ke show_sectionC1 false"
		return show_sectionC1(request, False)

@login_required(login_url='core:login')
def update_sectionC1(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		c1_obj = CMother.objects.get(c_form_id=request.session['form_id'])
		c1_obj = save_sectionC1(c1_obj, request)
		print "masuk ke show_sectionC1 yang diupdate true"
		return show_sectionC1(request, True)
	else:
		print "masuk ke show_sectionC1 yang diupdate false"
		return show_sectionC1(request, False)		


@login_required(login_url='core:login')
def show_sectionC1(request, is_save):
	form = CBirth.objects.get(id=request.session['form_id'])	
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
		print form.id		
		c1_obj = CMother.objects.get(c_form_id=form.id)
		print c1_obj
		blood_test_date = c1_obj.c1m_blood_test_date.strftime('%Y-%m-%d')
		print blood_test_date			
		swab_date = c1_obj.c1m_swab_date.strftime('%Y-%m-%d')
		print swab_date
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:				
				return render(request, 'forms_c/sectionC1.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'c1' : c1_obj, 'blood_test_date' : blood_test_date, 'swab_date' : swab_date })
			else:
				print 'b'
				return render(request, 'forms_c/sectionC1.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'c1' : c1_obj, 'blood_test_date' : blood_test_date, 'swab_date' : swab_date })
		else:
			print 'c'
			if is_save:	
				print 'masuk ke yang is_save = true '
				return render(request, 'forms_c/sectionC1.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'c1' : c1_obj, 'blood_test_date' : blood_test_date, 'swab_date' : swab_date})
			else:
				print 'masuk ke yang is_save = false'
				return render(request, 'forms_c/sectionC1.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'c1' : c1_obj, 'blood_test_date' : blood_test_date, 'swab_date' : swab_date})	
	except:
		print 'masuk ke except'
		return render(request, 'forms_c/sectionC1.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

def save_sectionC1(c1_obj, request):
	c1_obj.c1m_ur_number = request.POST.get('c1m_ur_number')
	c1_obj.c1m_delivery_place = request.POST.get('c1m_delivery_place')
	c1_obj.c1m_gestational_age_fdlm = request.POST.get('c1m_gestational_age_fdlm')
	c1_obj.c1m_gestational_age_usg = request.POST.get('c1m_gestational_age_usg')
	c1_obj.c1m_systolic1st = request.POST.get('c1m_systolic1st')
	c1_obj.c1m_systolic2nd = request.POST.get('c1m_systolic2nd')
	c1_obj.c1m_diastolic1st = request.POST.get('c1m_diastolic1st')
	c1_obj.c1m_diastolic2nd = request.POST.get('c1m_diastolic2nd')
	c1_obj.c1m_delivery_weight = request.POST.get('c1m_delivery_weight')
	c1_obj.c1m_delivery_method = request.POST.get('c1m_delivery_method')	 

	if request.POST.get('c1m_delivery_compilation') == '1':
		c1_obj.c1m_delivery_compilation = True
	else:
		c1_obj.c1m_delivery_compilation = False		

	if request.POST.get('c1m_hypertensioncom') == 'on':
		c1_obj.c1m_hypertensioncom = True
	else:
		c1_obj.c1m_hypertensioncom = False

	if request.POST.get('c1m_eclampsiacom') == 'on':
		c1_obj.c1m_eclampsiacom = True
	else:
		c1_obj.c1m_eclampsiacom = False
	 
	if request.POST.get('c1m_visualcom') == 'on' :
	 	c1_obj.c1m_visualcom = True
	else:
	 	c1_obj.c1m_visualcom = False

	if request.POST.get('c1m_consciousnesscom') == 'on':
	 	c1_obj.c1m_consciousnesscom = True
	else:
	 	c1_obj.c1m_consciousnesscom =  False

	if request.POST.get('c1m_seizurecom') == 'on':
	 	c1_obj.c1m_seizurecom = True
	else:
	 	c1_obj.c1m_seizurecom = False

	if request.POST.get('c1m_pullmonarycom') == 'on':
	 	c1_obj.c1m_pullmonarycom = True
	else:
	 	c1_obj.c1m_pullmonarycom = False

	if request.POST.get('c1m_postpartumcom') == 'on':
	 	c1_obj.c1m_postpartumcom = True
	else:
	 	c1_obj.c1m_postpartumcom = False

	if request.POST.get('c1m_fevercom') == 'on':
	 	c1_obj.c1m_fevercom = True
	else:
	 	c1_obj.c1m_fevercom = False

	if request.POST.get('c1m_prematurerupturecom') == 'on':
	 	c1_obj.c1m_prematurerupturecom = True
	else:
	 	c1_obj.c1m_prematurerupturecom = False

	if request.POST.get('c1m_placentacom') == 'on':
	 	c1_obj.c1m_placentacom = True
	else:
	 	c1_obj.c1m_placentacom = False

	if request.POST.get('c1m_placenta_previacom') == 'on':
	 	c1_obj.c1m_placenta_previacom = True
	else:
	 	c1_obj.c1m_placenta_previacom = False

	if request.POST.get('c1m_gbscom') == 'on':
	 	c1_obj.c1m_gbscom = True
	else:
	 	c1_obj.c1m_gbscom = False

	if request.POST.get('c1m_chorioamnionitiscom') == 'on':
	 	c1_obj.c1m_chorioamnionitiscom = True
	else:
	 	c1_obj.c1m_chorioamnionitiscom = False

	if request.POST.get('c1m_chlinical_diagnosiscom') == 'on':
	 	c1_obj.c1m_chlinical_diagnosiscom = True
	else:
	 	c1_obj.c1m_chlinical_diagnosiscom = False

	if request.POST.get('c1m_definite_diagnosiscom') == 'on':
	 	c1_obj.c1m_definite_diagnosiscom = True
	else:
	 	c1_obj.c1m_definite_diagnosiscom = False

	if request.POST.get('c1m_othercom') == 'on':
	 	c1_obj.c1m_othercom = True
	else:
	 	c1_obj.c1m_othercom = False		 


	c1_obj.c1m_antibiotics = request.POST.get('c1m_antibiotics')
	c1_obj.c1m_antibiotics_type = request.POST.get('c1m_antibiotics_type')
	c1_obj.c1m_antibiotics_indication = request.POST.get('c1m_antibiotics_indication')
	c1_obj.c1m_antibiotics_duration = request.POST.get('c1m_antibiotics_duration')
	c1_obj.c1m_proteinuria = request.POST.get('c1m_proteinuria')
	c1_obj.c1m_delivery_blood_test = request.POST.get('c1m_delivery_blood_test')
	if request.POST.get('c1m_blood_test_date'):		
		c1_obj.c1m_blood_test_date = request.POST.get('c1m_blood_test_date')
	else:
		c1_obj.c1m_blood_test_date = None

	c1_obj.c1m_hb = request.POST.get('c1m_hb')
	c1_obj.c1m_wbc = request.POST.get('c1m_wbc')
	c1_obj.c1m_platelets = request.POST.get('c1m_platelets')
	c1_obj.c1m_sgot = request.POST.get('c1m_sgot')
	c1_obj.c1m_sgpt = request.POST.get('c1m_sgpt')
	c1_obj.c1m_ureum = request.POST.get('c1m_ureum')
	c1_obj.c1m_creatinine = request.POST.get('c1m_creatinine')
	c1_obj.c1m_vaginal_swab = request.POST.get('c1m_vaginal_swab')
	
	if request.POST.get('c1m_swab_date'):
		c1_obj.c1m_swab_date = request.POST.get('c1m_swab_date')
		
	else:
		c1_obj.c1m_swab_date = None			
	c1_obj.save()
	return c1_obj


###Controller Section 2

def process_sectionC2(request):
	if request.POST.get('form_id'):
		request.session['form_id'] = request.POST.get('form_id')
	c_form_obj = CBirth.objects.get(id=int(request.session['form_id']))
	try:
		c2_obj = CPlacentalSampling.objects.get(c_form=c_form_obj)
		print "masuk ke update sectionC2"		
		return update_sectionC2(request)	
	except:		
		return create_sectionC2(request)

def create_sectionC2(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		c_form_obj = CBirth.objects.get(id=request.session['form_id'])
		c2_obj = CPlacentalSampling()
		c2_obj.c_form = c_form_obj
		c2_obj = save_sectionC2(c2_obj, request)		
		return show_sectionC2(request, True)	
	else:		
		return show_sectionC2(request, False)

@login_required(login_url='core:login')
def update_sectionC2(request):
	
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		c2_obj = CPlacentalSampling.objects.get(c_form_id=request.session['form_id'])
		c2_obj = save_sectionC2(c2_obj, request)
		print "masuk ke show_sectionC2(pada method update) true "
		return show_sectionC2(request, True)
	else:
		print "masuk ke show_sectionC2 false"
		return show_sectionC2(request, False)

@login_required(login_url='core:login')
def show_sectionC2(request, is_save):
	print 's'
	form = CBirth.objects.get(id=request.session['form_id'])		
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
		c2_obj = CPlacentalSampling.objects.get(c_form_id=form.id)		
		sampling_date = c2_obj.c2m_sampling_date.strftime('%Y-%m-%d')		
		sampling_time = c2_obj.c2m_sampling_time.strftime('%H:%M')		
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				print 'a'
				return render(request, 'forms_c/sectionC2.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'c2' : c2_obj, 'sampling_date' : sampling_date, 'sampling_time' : sampling_time})
			else:
				print 'b'
				return render(request, 'forms_c/sectionC2.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'c2' : c2_obj, 'sampling_date' : sampling_date, 'sampling_time' : sampling_time })
		else:			
			if is_save:					
				return render(request, 'forms_c/sectionC2.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'c2' : c2_obj, 'sampling_date' : sampling_date, 'sampling_time' : sampling_time })
			else:
				return render(request, 'forms_c/sectionC2.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'c2' : c2_obj, 'sampling_date' : sampling_date, 'sampling_time' : sampling_time })	
	except:
		print 'd'
		return render(request, 'forms_c/sectionC2.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})


def save_sectionC2(c2_obj, request):
	c2_obj.c2m_sampling_date = request.POST.get('c2m_sampling_date')
	c2_obj.c2m_sampling_time = request.POST.get('c2m_sampling_time')
	if request.POST.get('c2m_pictures_taken') == "1":
		c2_obj.c2m_pictures_taken = 1
	else:
		c2_obj.c2m_pictures_taken = 0

	print c2_obj.c2m_pictures_taken

	# if  request.POST.get('c2m_comments') == "1":
	# 	c2_obj.c2m_comments = True
	# else:
	# 	c2_obj.c2m_comments = False
	 
	#c2_obj.c2m_pictures_taken = request.POST.get('c2m_pictures_taken')
	c2_obj.c2m_comments = request.POST.get('c2m_comments')
	c2_obj.c2m_placenta_shapes = request.POST.get('c2m_placenta_shapes')
	c2_obj.c2m_placenta_shapes_other = request.POST.get('c2m_placenta_shapes_other')
	c2_obj.c2m_umbilical_cord = request.POST.get('c2m_umbilical_cord')
	c2_obj.c2m_abnormality = request.POST.get('c2m_abnormality')
	c2_obj.c2m_cord_blood_sample = request.POST.get('c2m_cord_blood_sample')
	c2_obj.c2m_membrane_roll = request.POST.get('c2m_membrane_roll')
	c2_obj.c2m_membrane_trim = request.POST.get('c2m_membrane_trim')
	c2_obj.c2m_membrane_weight =  request.POST.get('c2m_membrane_weight')
	c2_obj.c2m_villous_tissue = request.POST.get('c2m_villous_tissue')
	c2_obj.c2m_placenta_container = request.POST.get('c2m_placenta_container')
	c2_obj.c2m_placenta_laboratory = request.POST.get('c2m_placenta_laboratory')
	c2_obj.c2m_placenta_sampling = request.POST.get('c2m_placenta_sampling')
	c2_obj.save()
	return c2_obj


### Controller Section 3
@login_required(login_url='core:login')
def process_sectionC3(request):	 
	if request.POST.get('form_id'):	
		request.session['form_id'] = request.POST.get('form_id')
	c_form_obj = CInfantData.objects.get(id=int(request.session['form_id']))	
	try:
		c3_obj = CInfantData.objects.get(c_form=c_form_obj)
		print "masuk ke update_sectionC1"		
		return update_sectionC3(request)		
	except:
		print "masuk ke create_sectionC1"				
		return create_sectionC3(request)


@login_required(login_url='core:login')
def create_sectionC3(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		c_form_obj = CBirth.objects.get(id=request.session['form_id'])
		c3_obj = CInfantData()
		c3_obj.c_form = c_form_obj
		c3_obj = save_sectionC3(c3_obj, request)
		print "masuk ke show_sectionC1 true"		
		return show_sectionC3(request, True)	
	else:		
		print "masuk ke show_sectionC1 false"
		return show_sectionC3(request, False)

@login_required(login_url='core:login')
def update_sectionC3(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		c3_obj = CInfantData.objects.get(c_form_id=request.session['form_id'])
		c3_obj = save_sectionC3(c3_obj, request)
		print "masuk ke show_sectionC1 yang diupdate true"
		return show_sectionC3(request, True)
	else:
		print "masuk ke show_sectionC1 yang diupdate false"
		return show_sectionC3(request, False)

@login_required(login_url='core:login')
def show_sectionC3(request, is_save):	
	form = CInfantData.objects.get(id=request.session['form_id'])	
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
		c3_obj = CInfantData.objects.get(c_form_id=form.id)		
		date_of_birth = c3_obj.c3c_dob.strftime('%Y-%m-%d')
		blood_test_date = c3_obj.c3c_blood_test_date.strftime('%Y-%m-%d')
		coord_blood_date = c3_obj.c3c_cord_blood_date.strftime('%Y-%m-%d')
		mother_discharge_date = c3_obj.c4m_discharge_date.strftime('%Y-%m-%d')
		baby_discharge_date = c3_obj.c4c_discharge_date.strftime('%Y-%m-%d')			
		
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:				
				return render(request, 'forms_c/sectionC3.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'c3' : c3_obj, 'blood_test_date' : blood_test_date, 'coord_blood_date' : coord_blood_date, 'mother_discharge_date' : mother_discharge_date, 'baby_discharge_date' : baby_discharge_date })
			else:
				print 'b'
				return render(request, 'forms_c/sectionC3.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'c3' : c3_obj, 'blood_test_date' : blood_test_date, 'coord_blood_date' : coord_blood_date, 'mother_discharge_date' : mother_discharge_date, 'baby_discharge_date' : baby_discharge_date })
		else:
			print 'c'
			if is_save:	
				print 'masuk ke yang is_save = true '
				return render(request, 'forms_c/sectionC3.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'c3' : c3_obj, 'blood_test_date' : blood_test_date, 'coord_blood_date' : coord_blood_date, 'mother_discharge_date' : mother_discharge_date, 'baby_discharge_date' : baby_discharge_date})
			else:
				print 'masuk ke yang is_save = false'
				return render(request, 'forms_c/sectionC3.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'c3' : c3_obj, 'blood_test_date' : blood_test_date, 'coord_blood_date' : coord_blood_date, 'mother_discharge_date' : mother_discharge_date, 'baby_discharge_date' : baby_discharge_date})	
	except:
		print 'masuk ke except'
		return render(request, 'forms_c/sectionC3.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})
 












