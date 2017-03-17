from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
import datetime


@login_required(login_url='core:login')
def check_form(request):
	form = ABaseLine.objects.get(id=request.session['form_id'])
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
		a1_obj = A1MotherDemographic.objects.get(a_form_id=request.session['form_id']) 
		dob = a1_obj.a1m_dob.strftime('%Y-%m-%d')
		moving_date = a1_obj.a1m_moving_date.strftime('%Y-%m-%d')
		return render(request, 'forms/section1.html', {'date_data_checked' : date_data_checked, 'success' : success, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : a1_obj, 'dob' : dob, 'moving_date' : moving_date})
	except:
		return render(request, 'forms/section1.html', {'date_data_checked' : date_data_checked, 'success' : success, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def save_form(request):
	form = ABaseLine.objects.get(id=request.session['form_id'])
	form.is_save_all = True
	form.save()
	return show_section1(request, request.session['form_id'])

@login_required(login_url='core:login')
def edit_form(request):
	form = ABaseLine.objects.get(id=request.session['form_id'])
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
			a1_obj = A1MotherDemographic.objects.get(a_form_id=request.session['form_id']) 
			dob = a1_obj.a1m_dob.strftime('%Y-%m-%d')
			moving_date = a1_obj.a1m_moving_date.strftime('%Y-%m-%d')
			if form.date_data_checked is not None:
				date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
				return render(request, 'forms/edit_section1.html', {'date_data_checked' : date_data_checked,'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : a1_obj, 'dob' : dob, 'moving_date' : moving_date})
			else:	
				return render(request, 'forms/edit_section1.html', {'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : a1_obj, 'dob' : dob, 'moving_date' : moving_date})
		except:
				return render(request, 'forms/edit_section1.html', {'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})
	else:
		return render(request, 'forms/edit_section1.html', {'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})					

@login_required(login_url='core:login')
def create_form(request):
	if request.method == "POST":
		a_obj = ABaseLine()
		a_obj.participant_id = request.session['participant_id']	
		a_obj.interviewer_id = request.POST.get('interviewer_id')
		a_obj.data_entry_id = request.user.username
		a_obj.date_admission = request.POST.get('date_admission')
		a_obj.date_interviewed = request.POST.get('date_interviewed')
		a_obj.date_data_entered = request.POST.get('date_data_entered')
		a_obj.save()
		request.session['form_id'] = a_obj.id
		return process_section1(request)
	else:
		participant = Participant.objects.get(id=request.session['participant_id'])
		date_admission = participant.date_admission.strftime('%Y-%m-%d')
		staff_list = User.objects.filter(is_staff=False)
		return render(request, 'forms/form.html', {'staff_list' : staff_list, 'context' : 'create', 'participant' : participant, 'date_admission' : date_admission})



###### CONTROLLER SECTION1
@login_required(login_url='core:login')
def process_section1(request):
	if request.POST.get('form_id'):
		request.session['form_id'] = request.POST.get('form_id')
	a_form_obj = ABaseLine.objects.get(id=int(request.session['form_id']))
	try:
		a1_obj = A1MotherDemographic.objects.get(a_form=a_form_obj)
		print "masuk ke update_section1"
		return update_section1(request)	
	except:
		print "masuk ke create_section1"
		return create_section1(request)

@login_required(login_url='core:login')
def create_section1(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		a_form_obj = ABaseLine.objects.get(id=request.session['form_id'])
		a1_obj = A1MotherDemographic()
		a1_obj.a_form = a_form_obj
		a1_obj = save_section1(a1_obj, request)
		print "masuk ke show section true"
		return show_section1(request, True)	
	else:
		print "masuk ke show section false"
		return show_section1(request, False)
		
@login_required(login_url='core:login')
def update_section1(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		a1_obj = A1MotherDemographic.objects.get(a_form_id=request.session['form_id'])
		a1_obj = save_section1(a1_obj, request)
		print "masuk ke show section yang diupdate true"
		return show_section1(request, True)	
	else:
		print "masuk ke show section1 yang diupdate false"
		return show_section1(request, False)		

@login_required(login_url='core:login')
def show_section1(request, is_save):
	form = ABaseLine.objects.get(id=request.session['form_id'])
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
		a1_obj = A1MotherDemographic.objects.get(a_form_id=form.id) 
		dob = a1_obj.a1m_dob.strftime('%Y-%m-%d')		
		moving_date = a1_obj.a1m_moving_date.strftime('%Y-%m-%d')		
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				return render(request, 'forms/section1.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : a1_obj, 'dob' : dob, 'moving_date' : moving_date, 'date_data_checked' : date_data_checked})
			else:
				print 'b'
				return render(request, 'forms/section1.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : a1_obj, 'dob' : dob, 'moving_date' : moving_date, 'date_data_checked' : date_data_checked})
		else:
			print 'c'
			if is_save:	
				print 'masuk ke yang is_save = true '
				return render(request, 'forms/section1.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : a1_obj, 'dob' : dob, 'moving_date' : moving_date})
			else:
				print 'masuk ke yang is_save = false'
				return render(request, 'forms/section1.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a1' : a1_obj, 'dob' : dob, 'moving_date' : moving_date})	
	except:
		print "masuk ke except yang form A"
		return render(request, 'forms/section1.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section1(a1_obj, request):
	a1_obj.a1m_name = request.POST.get('a1m_name')
	a1_obj.a1m_pob = request.POST.get('a1m_pob')
	a1_obj.a1m_dob = request.POST.get('a1m_dob')
	a1_obj.a1m_residence_street = request.POST.get('a1m_residence_street')
	a1_obj.a1m_residence_rt = request.POST.get('a1m_residence_rt')
	a1_obj.a1m_residence_rw = request.POST.get('a1m_residence_rw')
	a1_obj.a1m_residence_district = request.POST.get('a1m_residence_district')
	a1_obj.a1m_residence_city = request.POST.get('a1m_residence_city')
	a1_obj.a1m_residence_zipcode = request.POST.get('a1m_residence_zipcode')
	a1_obj.a1m_moving_date = request.POST.get('a1m_moving_date')
	a1_obj.a1m_residing_duration = request.POST.get('a1m_residing_duration')
	a1_obj.a1m_residential_status = request.POST.get('a1m_residential_status')
		##
	if request.POST.get('a1m_previous_residence_1st_start_year'):	
		a1_obj.a1m_previous_residence_1st_start_year = request.POST.get('a1m_previous_residence_1st_start_year')
		a1_obj.a1m_previous_residence_1st_end_year = request.POST.get('a1m_previous_residence_1st_end_year')
		a1_obj.a1m_previous_residence_1st_district = request.POST.get('a1m_previous_residence_1st_district')
		a1_obj.a1m_previous_residence_1st_city = request.POST.get('a1m_previous_residence_1st_city')
		a1_obj.a1m_previous_residence_1st_zipcode = request.POST.get('a1m_previous_residence_1st_zipcode')	
		###
	else:
		a1_obj.a1m_previous_residence_1st_start_year = None
		a1_obj.a1m_previous_residence_1st_end_year = None
		a1_obj.a1m_previous_residence_1st_district = ""
		a1_obj.a1m_previous_residence_1st_city = ""
		a1_obj.a1m_previous_residence_1st_zipcode = ""
	
	if request.POST.get('a1m_previous_residence_2nd_start_year'):	
		a1_obj.a1m_previous_residence_2nd_start_year = request.POST.get('a1m_previous_residence_2nd_start_year')
		a1_obj.a1m_previous_residence_2nd_end_year = request.POST.get('a1m_previous_residence_2nd_end_year')
		a1_obj.a1m_previous_residence_2nd_district = request.POST.get('a1m_previous_residence_2nd_district')
		a1_obj.a1m_previous_residence_2nd_city = request.POST.get('a1m_previous_residence_2nd_city')
		a1_obj.a1m_previous_residence_2nd_zipcode = request.POST.get('a1m_previous_residence_2nd_zipcode')
	else:
		a1_obj.a1m_previous_residence_2nd_start_year = None
		a1_obj.a1m_previous_residence_2nd_end_year = None
		a1_obj.a1m_previous_residence_2nd_district = ""
		a1_obj.a1m_previous_residence_2nd_city = ""
		a1_obj.a1m_previous_residence_2nd_zipcode = ""

		##
	if request.POST.get('a1m_previous_residence_3rd_start_year'):	
		a1_obj.a1m_previous_residence_3rd_start_year = request.POST.get('a1m_previous_residence_3rd_start_year')
		a1_obj.a1m_previous_residence_3rd_end_year = request.POST.get('a1m_previous_residence_3rd_end_year')
		a1_obj.a1m_previous_residence_3rd_district = request.POST.get('a1m_previous_residence_3rd_district')
		a1_obj.a1m_previous_residence_3rd_city = request.POST.get('a1m_previous_residence_3rd_city')
		a1_obj.a1m_previous_residence_3rd_zipcode = request.POST.get('a1m_previous_residence_3rd_zipcode')
	else:
		a1_obj.a1m_previous_residence_3rd_start_year = None
		a1_obj.a1m_previous_residence_3rd_end_year = None
		a1_obj.a1m_previous_residence_3rd_district = ""
		a1_obj.a1m_previous_residence_3rd_city = ""
		a1_obj.a1m_previous_residence_3rd_zipcode = ""
		##
	if request.POST.get('a1m_previous_residence_4th_start_year'):	
		a1_obj.a1m_previous_residence_4th_start_year = request.POST.get('a1m_previous_residence_4th_start_year')
		a1_obj.a1m_previous_residence_4th_end_year = request.POST.get('a1m_previous_residence_4th_end_year')
		a1_obj.a1m_previous_residence_4th_district = request.POST.get('a1m_previous_residence_4th_district')
		a1_obj.a1m_previous_residence_4th_city = request.POST.get('a1m_previous_residence_4th_city')
		a1_obj.a1m_previous_residence_4th_zipcode = request.POST.get('a1m_previous_residence_4th_zipcode')
	else:
		a1_obj.a1m_previous_residence_4th_start_year = None
		a1_obj.a1m_previous_residence_4th_end_year = None
		a1_obj.a1m_previous_residence_4th_district = ""
		a1_obj.a1m_previous_residence_4th_city = ""
		a1_obj.a1m_previous_residence_4th_zipcode = ""

		##
	if request.POST.get('a1m_previous_residence_5th_start_year'):	
		a1_obj.a1m_previous_residence_5th_start_year = request.POST.get('a1m_previous_residence_5th_start_year')
		a1_obj.a1m_previous_residence_5th_end_year = request.POST.get('a1m_previous_residence_5th_end_year')
		a1_obj.a1m_previous_residence_5th_district = request.POST.get('a1m_previous_residence_5th_district')
		a1_obj.a1m_previous_residence_5th_city = request.POST.get('a1m_previous_residence_5th_city')
		a1_obj.a1m_previous_residence_5th_zipcode = request.POST.get('a1m_previous_residence_5th_zipcode')
	else:
		a1_obj.a1m_previous_residence_5th_start_year = None
		a1_obj.a1m_previous_residence_5th_end_year = None
		a1_obj.a1m_previous_residence_5th_district = ""
		a1_obj.a1m_previous_residence_5th_city = ""
		a1_obj.a1m_previous_residence_5th_zipcode = ""

		##
	a1_obj.a1m_home_phone_number = request.POST.get('a1m_home_phone_number')
	a1_obj.a1m_mobile_phone_number = request.POST.get('a1m_mobile_phone_number')
	if request.POST.get('a1m_email'):
		a1_obj.a1m_email = request.POST.get('a1m_email')
	else:
		a1_obj.a1m_email = ""	
	a1_obj.a1m_education_level = request.POST.get('a1m_education_level')
	a1_obj.a1m_family_income = request.POST.get('a1m_family_income')
	a1_obj.a1m_marital_status = request.POST.get('a1m_marital_status')
		##
	a1_obj.a1m_relative_name = request.POST.get('a1m_relative_name')
	a1_obj.a1m_relative_street = request.POST.get('a1m_relative_street')
	a1_obj.a1m_relative_rt = request.POST.get('a1m_relative_rt')
	a1_obj.a1m_relative_rw = request.POST.get('a1m_relative_rw')
	a1_obj.a1m_relative_district = request.POST.get('a1m_relative_district')
	a1_obj.a1m_relative_city = request.POST.get('a1m_relative_city')
	a1_obj.a1m_relative_zipcode = request.POST.get('a1m_relative_zipcode')
	a1_obj.a1m_relative_home_phone_number = request.POST.get('a1m_relative_home_phone_number')
	a1_obj.a1m_relative_mobile_phone_number = request.POST.get('a1m_relative_mobile_phone_number')
	a1_obj.save()
	return a1_obj



###### CONTROLLER SECTION2
@login_required(login_url='core:login')
def process_section2(request):
	if request.POST.get('form_id'):
		request.session['form_id'] = request.POST.get('form_id')
	a_form_obj = ABaseLine.objects.get(id=int(request.session['form_id']))
	try:
		a2_obj = A2MotherEmployment.objects.get(a_form=a_form_obj)
		return update_section2(request)	
	except:
		return create_section2(request)

@login_required(login_url='core:login')
def create_section2(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		a_form_obj = ABaseLine.objects.get(id=request.session['form_id'])
		a2_obj = A2MotherEmployment()
		a2_obj.a_form = a_form_obj
		a2_obj = save_section2(a2_obj, request)
		return show_section2(request, True)	
	else:
		return show_section2(request, False)
		
@login_required(login_url='core:login')
def update_section2(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		a2_obj = A2MotherEmployment.objects.get(a_form_id=request.session['form_id'])
		a2_obj = save_section2(a2_obj, request)
		return show_section2(request, True)	
	else:
		return show_section2(request, False)		

@login_required(login_url='core:login')
def show_section2(request, is_save):
	form = ABaseLine.objects.get(id=request.session['form_id'])
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
		a2_obj = A2MotherEmployment.objects.get(a_form_id=form.id) 
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				return render(request, 'forms/section2.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a2' : a2_obj})
			else:
				return render(request, 'forms/section2.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a2' : a2_obj})
		else:
			if is_save:	
				return render(request, 'forms/section2.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a2' : a2_obj})
			else:
				return render(request, 'forms/section2.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a2' : a2_obj})	
	except:
		return render(request, 'forms/section2.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section2(a2_obj, request):
	a2_obj.a2m_working_status = request.POST.get('a2m_working_status')
	a2_obj.a2m_working_type = request.POST.get('a2m_working_type')
	if request.POST.get('a2m_working_pregnancy') == '1':
		a2_obj.a2m_working_pregnancy = True
	else:
		a2_obj.a2m_working_pregnancy = False
	if request.POST.get('a2m_maternal_leave'):
		a2_obj.a2m_maternal_leave_duration = request.POST.get('a2m_maternal_leave_duration')
		a2m_maternal_leave = True
	else:
		a2_obj.a2m_maternal_leave_duration = None
		a2m_maternal_leave = False	
	a2_obj.a2m_work_street = request.POST.get('a2m_work_street')
	a2_obj.a2m_work_rt = request.POST.get('a2m_work_rt')
	a2_obj.a2m_work_rw = request.POST.get('a2m_work_rw')
	a2_obj.a2m_work_district = request.POST.get('a2m_work_district')
	a2_obj.a2m_work_city = request.POST.get('a2m_work_city')
	a2_obj.a2m_work_zipcode = request.POST.get('a2m_work_zip_code')
	a2_obj.a2m_work_phone_number = request.POST.get('a2m_work_phone')
	if request.POST.get('a2m_car') == 'on':
		a2_obj.a2m_travel_by_car = True
	else:
		a2_obj.a2m_travel_by_car = False	
	if request.POST.get('a2m_motorcycle') == 'on':
		a2_obj.a2m_travel_by_motorcycle = True
	else:
		a2_obj.a2m_travel_by_motorcycle = False
	if request.POST.get('a2m_cycling') == 'on':
		a2_obj.a2m_travel_by_cycling = True
	else:
		a2_obj.a2m_travel_by_cycling = False
	if request.POST.get('a2m_walking') == 'on':
		a2_obj.a2m_travel_by_walking = True
	else:
		a2_obj.a2m_travel_by_walking = False
	if request.POST.get('a2m_public') == 'on':
		a2_obj.a2m_travel_by_public_transport = True
		a2_obj.a2m_public_transport_type = request.POST.get('a2m_public_transport')
	else:
		a2_obj.a2m_travel_by_public_transport = False
		a2_obj.a2m_public_transport_type = ""	
	if request.POST.get('a2m_time_travel'):
		a2_obj.a2m_work_time_travel = request.POST.get('a2m_time_travel')
	else:
		a2_obj.a2m_work_time_travel = None	
	if request.POST.get('a2m_pollutant') == '1':
		a2_obj.a2m_is_exposed_to_pollution = True
	else:
		a2_obj.a2m_is_exposed_to_pollution = False	
	if request.POST.get('a2m_working_hours'):	
		a2_obj.a2m_working_hours = request.POST.get('a2m_working_hours')
	else:
		a2_obj.a2m_working_hours = None
	a2_obj.a2m_working_area = request.POST.get('a2m_working_area')
	a2_obj.save()
	return a2_obj



###### CONTROLLER SECTION3
@login_required(login_url='core:login')
def process_section3(request):
	if request.POST.get('form_id'):
		request.session['form_id'] = request.POST.get('form_id')
	a_form_obj = ABaseLine.objects.get(id=int(request.session['form_id']))
	try:
		a3_obj = A3Obstetric.objects.get(a_form=a_form_obj)
		return update_section3(request)	
	except:
		return create_section3(request)

@login_required(login_url='core:login')
def create_section3(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		a_form_obj = ABaseLine.objects.get(id=request.session['form_id'])
		a3_obj = A3Obstetric()
		a3_obj.a_form = a_form_obj
		a3_obj = save_section3(a3_obj, request)
		return show_section3(request, True)	
	else:
		return show_section3(request, False)
		
@login_required(login_url='core:login')
def update_section3(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		a3_obj = A3Obstetric.objects.get(a_form_id=request.session['form_id'])
		a3_obj = save_section3(a3_obj, request)
		return show_section3(request, True)	
	else:
		return show_section3(request, False)

@login_required(login_url='core:login')
def show_section3(request, is_save):
	form = ABaseLine.objects.get(id=request.session['form_id'])
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
		a3_obj = A3Obstetric.objects.get(a_form_id=form.id)
		first_day_last_menstruation = a3_obj.a3m_first_day_last_menstruation.strftime('%Y-%m-%d')
		estimated_due_date = a3_obj.a3m_estimated_due_date.strftime('%Y-%m-%d') 
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				return render(request, 'forms/section3.html', {'estimated_due_date' : estimated_due_date, 'first_day_last_menstruation' : first_day_last_menstruation,'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a3' : a3_obj})
			else:
				return render(request, 'forms/section3.html', {'estimated_due_date' : estimated_due_date, 'first_day_last_menstruation' : first_day_last_menstruation, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a3' : a3_obj})
		else:
			if is_save:	
				return render(request, 'forms/section3.html', {'estimated_due_date' : estimated_due_date, 'first_day_last_menstruation' : first_day_last_menstruation, 'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a3' : a3_obj})
			else:
				return render(request, 'forms/section3.html', {'estimated_due_date' : estimated_due_date, 'first_day_last_menstruation' : first_day_last_menstruation, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a3' : a3_obj})	
	except:
		return render(request, 'forms/section3.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section3(a3_obj, request):
	a3_obj.a3m_pre_pregnancy_weight = request.POST.get('a3m_pre_weight')
	a3_obj.a3m_pre_pregnancy_height = request.POST.get('a3m_pre_height')
	a3_obj.a3m_first_day_last_menstruation = request.POST.get('a3m_fdlm')
	a3_obj.a3m_estimated_due_date = request.POST.get('a3m_edd')
	a3_obj.a3m_gravida = request.POST.get('a3m_gravida')
	a3_obj.a3m_parity = request.POST.get('a3m_parity')
	a3_obj.a3m_abortus = request.POST.get('a3m_abortus')
	
	if request.POST.get('a3m_premature') == "1":
		a3_obj.a3m_previous_premature = True
	else:
		a3_obj.a3m_previous_premature = False	
	
	if request.POST.get('a3m_miscarriage') == "1":
		a3_obj.a3m_previous_miscarriage = True
	else:
		a3_obj.a3m_previous_miscarriage = False
	
	###
	if request.POST.get('a3m_compilation') == "1":		
		a3_obj.a3m_previous_complication = True
	else:
		a3_obj.a3m_previous_complication = False
	if request.POST.get('a3m_hypertensioncom') == 'on':
		a3_obj.a3m_hypertension_complication = True
	else:
		a3_obj.a3m_hypertension_complication = False	
	if request.POST.get('a3m_diabetescom') == 'on':
		a3_obj.a3m_diabetes_complication = True
	else:
		a3_obj.a3m_diabetes_complication = False	
	if request.POST.get('a3m_preeclampsiacom') == 'on':
		a3_obj.a3m_preeclampsia_complication = True
	else:
		a3_obj.a3m_preeclampsia_complication = False	
	if request.POST.get('a3m_eclampsiacom') == 'on':
		a3_obj.a3m_eclampsia_complication = True
	else:
		a3_obj.a3m_eclampsia_complication = False	
	if request.POST.get('a3m_infectioncom') == 'on':
		a3_obj.a3m_infection_complication = True
	else:
		a3_obj.a3m_infection_complication = False	
	if request.POST.get('a3m_other') != '':
		a3_obj.a3m_other_complication = True
		a3_obj.a3m_other_complication_name = request.POST.get('a3m_other')
	else:
		a3_obj.a3m_other_complication = False
		a3_obj.a3m_other_complication_name = ""	
	
	###
	if request.POST.get('a3m_medicalhistory') == '1':	
		a3_obj.a3m_medical_history = True
	else:
		a3_obj.a3m_medical_history = False	
	if request.POST.get('a3m_asthmahis') == 'on':		
		a3_obj.a3m_asthma_history = True
	else:
		a3_obj.a3m_asthma_history = False	
	if request.POST.get('a3m_tbchis') == 'on':
		a3_obj.a3m_tubercolosis_history = True
	else:
		a3_obj.a3m_tubercolosis_history = False
	if request.POST.get('a3m_chroniccoughhis') == 'on':		
		a3_obj.a3m_cronic_cough_history = True
	else:
		a3_obj.a3m_cronic_cough_history = False	
	if request.POST.get('a3m_hypertensionhis') == 'on':
		a3_obj.a3m_hypertension_history = True
	else:
		a3_obj.a3m_hypertension_history = False
	
	###
	if request.POST.get('a3m_hdcoronary') == 'on':
		a3_obj.a3m_heart_disease_coronary = True
	else:
		a3_obj.a3m_heart_disease_coronary = False	
	if request.POST.get('a3m_hdvalve') == 'on':
		a3_obj.a3m_heart_disease_valve = True
	else:
		a3_obj.a3m_heart_disease_valve = False
	if request.POST.get('a3m_hdrhythm') == 'on':
		a3_obj.a3m_heart_disease_rhythm = True
	else:
		a3_obj.a3m_heart_disease_rhythm = False
	if request.POST.get('a3m_hdmuscle') == 'on':
		a3_obj.a3m_heart_disease_muscle = True
	else:
		a3_obj.a3m_heart_disease_muscle = False
	if a3_obj.a3m_heart_disease_coronary  or a3_obj.a3m_heart_disease_valve or a3_obj.a3m_heart_disease_rhythm  or a3_obj.a3m_heart_disease_muscle:
		a3_obj.a3m_heart_disease_history = True
	else:
		a3_obj.a3m_heart_disease_history =	False	
	
	###
	if request.POST.get('a3m_diabeteshis') == 'on':
		a3_obj.a3m_diabetes_history = True
	else:
		a3_obj.a3m_diabetes_history = False
	if request.POST.get('a3m_insulin') == 'on':
		a3_obj.a3m_is_use_insulin = True
	else:
		a3_obj.a3m_is_use_insulin = False
	if request.POST.get('a3m_strokehis') == 'on':
		a3_obj.a3m_stroke_history = True
	else:
		a3_obj.a3m_stroke_history = False
	if request.POST.get('a3m_allergyhis') != '':
		a3_obj.a3m_allergy_history = True
		a3_obj.a3m_allergy_detail = request.POST.get('a3m_allergyhis')
	else:
		a3_obj.a3m_allergy_history = False
		a3_obj.a3m_allergy_detail = ""	
	if request.POST.get('a3m_otherhis') != '':
		a3_obj.a3m_other_history = True
		a3_obj.a3m_other_detail = request.POST.get('a3m_otherhis')
	else:
		a3_obj.a3m_other_history = False
		a3_obj.a3m_other_detail = ""
	
	###
	if request.POST.get('a3m_diseaseFam') == "1":
		a3_obj.a3m_family_disease = True
	else:
		a3_obj.a3m_family_disease = False	
	if request.POST.get('a3m_asthma_fam_mother') == 'on':
		a3_obj.a3m_asthma_mother = True
	else:
		a3_obj.a3m_asthma_mother = False
	if request.POST.get('a3m_asthma_fam_father') == 'on':
		a3_obj.a3m_asthma_father = True
	else:
		a3_obj.a3m_asthma_father = False
	if request.POST.get('a3m_asthma_fam_siblings') == 'on':
		a3_obj.a3m_asthma_sibling = True
	else:
		a3_obj.a3m_asthma_sibling = False
	if request.POST.get('a3m_hypertension_fam_mother') == 'on':
		a3_obj.a3m_hypertension_mother = True
	else:
		a3_obj.a3m_hypertension_mother =  False
	if request.POST.get('a3m_hypertension_fam_father') == 'on':
		a3_obj.a3m_hypertension_father = True
	else:
		a3_obj.a3m_hypertension_father = False
	if request.POST.get('a3m_hypertension_fam_siblings') == 'on':
		a3_obj.a3m_hypertension_sibling = True
	else:
		a3_obj.a3m_hypertension_sibling = False
	if request.POST.get('a3m_hd_fam_mother') == 'on':
		a3_obj.a3m_heart_disease_mother = True
	else:
		a3_obj.a3m_heart_disease_mother = False
	if request.POST.get('a3m_hd_fam_father') == 'on':
		a3_obj.a3m_heart_disease_father = True
	else:
		a3_obj.a3m_heart_disease_father = False
	if request.POST.get('a3m_hd_fam_siblings') == 'on':
		a3_obj.a3m_heart_disease_sibling = True
	else:
		a3_obj.a3m_heart_disease_sibling = False
	if request.POST.get('a3m_diabetes_fam_mother') == 'on':
		a3_obj.a3m_diabetes_mother = True
	else:
		a3_obj.a3m_diabetes_mother = False
	if request.POST.get('a3m_diabetes_fam_father') == 'on':
		a3_obj.a3m_diabetes_father = True
	else:
		a3_obj.a3m_diabetes_father = False
	if request.POST.get('a3m_diabetes_fam_siblings') == 'on':
		a3_obj.a3m_diabetes_sibling = True
	else:
		a3_obj.a3m_diabetes_sibling = False
	if request.POST.get('a3m_stroke_fam_mother') == 'on':
		a3_obj.a3m_stroke_mother = True
	else:
		a3_obj.a3m_stroke_mother = False
	if request.POST.get('a3m_stroke_fam_father') == 'on':
		a3_obj.a3m_stroke_father = True
	else:
		a3_obj.a3m_stroke_father = False
	if request.POST.get('a3m_stroke_fam_siblings') == 'on':
		a3_obj.a3m_stroke_sibling = True
	else:
		a3_obj.a3m_stroke_sibling = False
	
	###
	if request.POST.get('a3m_other_desease') != '':
		a3_obj.a3m_other_disease = True
		a3_obj.a3m_other_disease_name = request.POST.get('a3m_other_desease')
	else:
		a3_obj.a3m_other_disease = False
		a3_obj.a3m_other_disease_name = ""

	if request.POST.get('a3m_other_fam_mother') == 'on':
		a3_obj.a3m_other_mother = True
	else:
		a3_obj.a3m_other_mother = False
	if request.POST.get('a3m_other_fam_father') == 'on':
		a3_obj.a3m_other_father = True
	else:
		a3_obj.a3m_other_father = False
	if request.POST.get('a3m_other_fam_siblings') == 'on':
		a3_obj.a3m_other_sibling = True
	else:
		a3_obj.a3m_other_sibling = False		
	a3_obj.save()
	return a3_obj




###### CONTROLLER SECTION4
@login_required(login_url='core:login')
def process_section4(request):
	if request.POST.get('form_id'):
		request.session['form_id'] = request.POST.get('form_id')
	a_form_obj = ABaseLine.objects.get(id=int(request.session['form_id']))
	try:
		a4_obj = A4Father.objects.get(a_form=a_form_obj)
		return update_section4(request)	
	except:
		return create_section4(request)

@login_required(login_url='core:login')
def create_section4(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		a_form_obj = ABaseLine.objects.get(id=request.session['form_id'])
		a4_obj = A4Father()
		a4_obj.a_form = a_form_obj
		a4_obj = save_section4(a4_obj, request)
		return show_section4(request, True)	
	else:
		return show_section4(request, False)
		
@login_required(login_url='core:login')
def update_section4(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		a4_obj = A4Father.objects.get(a_form_id=request.session['form_id'])
		a4_obj = save_section4(a4_obj, request)
		return show_section4(request, True)	
	else:
		return show_section4(request, False)

@login_required(login_url='core:login')
def show_section4(request, is_save):
	form = ABaseLine.objects.get(id=request.session['form_id'])
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
		a4_obj = A4Father.objects.get(a_form_id=form.id)
		dob = a4_obj.a4f_dob.strftime('%Y-%m-%d')
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				return render(request, 'forms/section4.html', {'dob' : dob, 'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a4' : a4_obj})
			else:
				return render(request, 'forms/section4.html', {'dob' : dob, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a4' : a4_obj})
		else:
			if is_save:	
				return render(request, 'forms/section4.html', {'dob' : dob, 'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a4' : a4_obj})
			else:
				return render(request, 'forms/section4.html', {'dob' : dob, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a4' : a4_obj})	
	except:
		return render(request, 'forms/section4.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section4(a4_obj, request):
	print "tes"
	a4_obj.a4f_name = request.POST.get('a4f_name')
	a4_obj.a4f_pob = request.POST.get('a4f_pob')
	a4_obj.a4f_dob = request.POST.get('a4f_dob')
	a4_obj.a4f_residence_street = request.POST.get('a4f_residence_street')
	a4_obj.a4f_residence_rt = request.POST.get('a4f_residence_rt')
	a4_obj.a4f_residence_rw = request.POST.get('a4f_residence_rw')
	a4_obj.a4f_residence_district = request.POST.get('a4f_residence_district')
	a4_obj.a4f_residence_city = request.POST.get('a4f_residence_city')
	a4_obj.a4f_residence_zipcode = request.POST.get('a4f_residence_zipcode')
	a4_obj.a4f_home_phone_number = request.POST.get('a4f_home_phone_number')
	a4_obj.a4f_mobile_phone_number = request.POST.get('a4f_mobile_phone_number')
	if request.POST.get('a4f_email'):
		a4_obj.a4f_email = request.POST.get('a4f_email')
	else:
		a4_obj.a4f_email = ""
	a4_obj.a4f_education_level = request.POST.get('a4f_education_level')
	a4_obj.a4f_weight = request.POST.get('a4f_education_level')
	a4_obj.a4f_height = request.POST.get('a4f_education_level')
	a4_obj.a4f_employment_status = request.POST.get('a4f_working_status')
	a4_obj.a4f_type_of_job = request.POST.get('a4f_working_type')
	a4_obj.a4f_work_street = request.POST.get('a4f_work_street')
	a4_obj.a4f_work_rt = request.POST.get('a4f_work_rt')
	a4_obj.a4f_work_rw = request.POST.get('a4f_work_rw')
	a4_obj.a4f_work_district = request.POST.get('a4f_work_district')
	a4_obj.a4f_work_city = request.POST.get('a4f_work_city')
	a4_obj.a4f_work_zipcode = request.POST.get('a4f_work_zip_code')
	a4_obj.a4f_work_phone_number = request.POST.get('a4f_work_phone')
	###
	if request.POST.get('a4f_medicalhistory') == '1':	
		a4_obj.a4f_medical_history = True
	else:
		a4_obj.a4f_medical_history = False	
	if request.POST.get('a4f_asthmahis') == 'on':		
		a4_obj.a4f_asthma_history = True
	else:
		a4_obj.a4f_asthma_history = False	
	if request.POST.get('a4f_tbchis') == 'on':
		a4_obj.a4f_tubercolosis_history = True
	else:
		a4_obj.a4f_tubercolosis_history = False
	if request.POST.get('a4f_chroniccoughhis') == 'on':		
		a4_obj.a4f_cronic_cough_history = True
	else:
		a4_obj.a4f_cronic_cough_history = False	
	if request.POST.get('a4f_hypertensionhis') == 'on':
		a4_obj.a4f_hypertension_history = True
	else:
		a4_obj.a4f_hypertension_history = False
	
	###
	if request.POST.get('a4f_hdcoronary') == 'on':
		a4_obj.a4f_heart_disease_coronary = True
	else:
		a4_obj.a4f_heart_disease_coronary = False	
	if request.POST.get('a4f_hdvalve') == 'on':
		a4_obj.a4f_heart_disease_valve = True
	else:
		a4_obj.a4f_heart_disease_valve = False
	if request.POST.get('a4f_hdrhythm') == 'on':
		a4_obj.a4f_heart_disease_rhythm = True
	else:
		a4_obj.a4f_heart_disease_rhythm = False
	if request.POST.get('a4f_hdmuscle') == 'on':
		a4_obj.a4f_heart_disease_muscle = True
	else:
		a4_obj.a4f_heart_disease_muscle = False
	if a4_obj.a4f_heart_disease_coronary  or a4_obj.a4f_heart_disease_valve or a4_obj.a4f_heart_disease_rhythm  or a4_obj.a4f_heart_disease_muscle:
		a4_obj.a4f_heart_disease_history = True
	else:
		a4_obj.a4f_heart_disease_history =	False	
	
	###
	if request.POST.get('a4f_diabeteshis') == 'on':
		a4_obj.a4f_diabetes_history = True
	else:
		a4_obj.a4f_diabetes_history = False
	if request.POST.get('a4f_insulin') == 'on':
		a4_obj.a4f_is_use_insulin = True
	else:
		a4_obj.a4f_is_use_insulin = False
	if request.POST.get('a4f_strokehis') == 'on':
		a4_obj.a4f_stroke_history = True
	else:
		a4_obj.a4f_stroke_history = False
	if request.POST.get('a4f_allergyhis') != '':
		a4_obj.a4f_allergy_history = True
		a4_obj.a4f_allergy_detail = request.POST.get('a4f_allergyhis')
	else:
		a4_obj.a4f_allergy_history = False
		a4_obj.a4f_allergy_detail = ""	
	if request.POST.get('a4f_otherhis') != '':
		a4_obj.a4f_other_history = True
		a4_obj.a4f_other_detail = request.POST.get('a4f_otherhis')
	else:
		a4_obj.a4f_other_history = False
		a4_obj.a4f_other_detail = ""
	
	###
	if request.POST.get('a4f_diseaseFam') == "1":
		a4_obj.a4f_family_disease = True
	else:
		a4_obj.a4f_family_disease = False	
	if request.POST.get('a4f_asthma_fam_mother') == 'on':
		a4_obj.a4f_asthma_mother = True
	else:
		a4_obj.a4f_asthma_mother = False
	if request.POST.get('a4f_asthma_fam_father') == 'on':
		a4_obj.a4f_asthma_father = True
	else:
		a4_obj.a4f_asthma_father = False
	if request.POST.get('a4f_asthma_fam_siblings') == 'on':
		a4_obj.a4f_asthma_sibling = True
	else:
		a4_obj.a4f_asthma_sibling = False
	if request.POST.get('a4f_hypertension_fam_mother') == 'on':
		a4_obj.a4f_hypertension_mother = True
	else:
		a4_obj.a4f_hypertension_mother =  False
	if request.POST.get('a4f_hypertension_fam_father') == 'on':
		a4_obj.a4f_hypertension_father = True
	else:
		a4_obj.a4f_hypertension_father = False
	if request.POST.get('a4f_hypertension_fam_siblings') == 'on':
		a4_obj.a4f_hypertension_sibling = True
	else:
		a4_obj.a4f_hypertension_sibling = False
	if request.POST.get('a4f_hd_fam_mother') == 'on':
		a4_obj.a4f_heart_disease_mother = True
	else:
		a4_obj.a4f_heart_disease_mother = False
	if request.POST.get('a4f_hd_fam_father') == 'on':
		a4_obj.a4f_heart_disease_father = True
	else:
		a4_obj.a4f_heart_disease_father = False
	if request.POST.get('a4f_hd_fam_siblings') == 'on':
		a4_obj.a4f_heart_disease_sibling = True
	else:
		a4_obj.a4f_heart_disease_sibling = False
	if request.POST.get('a4f_diabetes_fam_mother') == 'on':
		a4_obj.a4f_diabetes_mother = True
	else:
		a4_obj.a4f_diabetes_mother = False
	if request.POST.get('a4f_diabetes_fam_father') == 'on':
		a4_obj.a4f_diabetes_father = True
	else:
		a4_obj.a4f_diabetes_father = False
	if request.POST.get('a4f_diabetes_fam_siblings') == 'on':
		a4_obj.a4f_diabetes_sibling = True
	else:
		a4_obj.a4f_diabetes_sibling = False
	if request.POST.get('a4f_stroke_fam_mother') == 'on':
		a4_obj.a4f_stroke_mother = True
	else:
		a4_obj.a4f_stroke_mother = False
	if request.POST.get('a4f_stroke_fam_father') == 'on':
		a4_obj.a4f_stroke_father = True
	else:
		a4_obj.a4f_stroke_father = False
	if request.POST.get('a4f_stroke_fam_siblings') == 'on':
		a4_obj.a4f_stroke_sibling = True
	else:
		a4_obj.a4f_stroke_sibling = False
	
	###
	if request.POST.get('a4f_other_desease') != '':
		a4_obj.a4f_other_disease = True
		a4_obj.a4f_other_disease_name = request.POST.get('a4f_other_desease')
	else:
		a4_obj.a4f_other_disease = False
		a4_obj.a4f_other_disease_name = ""

	if request.POST.get('a4f_other_fam_mother') == 'on':
		a4_obj.a4f_other_mother = True
	else:
		a4_obj.a4f_other_mother = False
	if request.POST.get('a4f_other_fam_father') == 'on':
		a4_obj.a4f_other_father = True
	else:
		a4_obj.a4f_other_father = False
	if request.POST.get('a4f_other_fam_siblings') == 'on':
		a4_obj.a4f_other_sibling = True
	else:
		a4_obj.a4f_other_sibling = False
	a4_obj.save()
	return a4_obj


###### CONTROLLER SECTION5
@login_required(login_url='core:login')
def process_section5(request):
	if request.POST.get('form_id'):
		request.session['form_id'] = request.POST.get('form_id')
	a_form_obj = ABaseLine.objects.get(id=int(request.session['form_id']))
	try:
		a5_obj = A5PrePregnancySmoking.objects.get(a_form=a_form_obj)
		print "masuk1"
		return update_section5(request)	
	except:
		print "masuk2"
		return create_section5(request)

@login_required(login_url='core:login')
def create_section5(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		a_form_obj = ABaseLine.objects.get(id=request.session['form_id'])
		a5_obj = A5PrePregnancySmoking()
		a5_obj.a_form = a_form_obj
		a5_obj = save_section5(a5_obj, request)
		print "masuk3"
		return show_section5(request, True)	
	else:
		return show_section5(request, False)
		
@login_required(login_url='core:login')
def update_section5(request):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		a5_obj = A5PrePregnancySmoking.objects.get(a_form_id=request.session['form_id'])
		a5_obj = save_section5(a5_obj, request)
		print "masuk4"
		return show_section5(request, True)	
	else:
		return show_section5(request, False)

@login_required(login_url='core:login')
def show_section5(request, is_save):
	form = ABaseLine.objects.get(id=request.session['form_id'])
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
		a5_obj = A5PrePregnancySmoking.objects.get(a_form_id=form.id)
		print "masuk5" 
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked.strftime('%Y-%m-%d')
			if is_save:
				return render(request, 'forms/section5.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a5' : a5_obj})
			else:
				return render(request, 'forms/section5.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a5' : a5_obj})
		else:
			if is_save:	
				return render(request, 'forms/section5.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a5' : a5_obj})
			else:
				return render(request, 'forms/section5.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'a5' : a5_obj})	
	except:
		return render(request, 'forms/section5.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

#@login_required(login_url='core:login')
def save_section5(a5_obj, request):
	a5_obj.a5m_mother_smoking_status = request.POST.get('a5m_presmoking_status')
	if request.POST.get('a5m_quitting_duration'):
		a5_obj.a5m_mother_quit_duration = request.POST.get('a5m_quitting_duration')
	else:
		a5_obj.a5m_mother_quit_duration = 0	
	a5_obj.a5m_mother_start_smoke_age = request.POST.get('a5m_starting_age')
	a5_obj.a5m_mother_cigarretes_per_day = request.POST.get('a5m_cigar_number')
	if request.POST.get('a5m_cigar_type') == "1":
		a5_obj.a5m_mother_smoke_pipes = True
	else:
		a5_obj.a5m_mother_smoke_pipes = False
	if request.POST.get('a5m_household_smoker') == "1":
		a5_obj.a5m_other_member_smoke = True
	else:
		a5_obj.a5m_other_member_smoke = False
	a5_obj.a5m_other_member_smoke_number = request.POST.get('a5m_household_smoker_number')
	a5_obj.a5m_total_cigarretes_per_day = request.POST.get('a5m_household_total_cigar')
	if request.POST.get('a5m_household_presence') == "1":
		a5_obj.a5m_smoke_in_front_of = True
	else:
		a5_obj.a5m_smoke_in_front_of = False	
	
	##
	a5_obj.a5f_father_smoking_status = request.POST.get('a5f_presmoking_status')
	if request.POST.get('a5f_quitting_duration'):
		a5_obj.a5f_father_quit_duration = request.POST.get('a5f_quitting_duration')
	else:
		a5_obj.a5f_father_quit_duration = 0	
	a5_obj.a5f_father_start_smoke_age = request.POST.get('a5f_starting_age')
	a5_obj.a5f_father_cigarretes_per_day = request.POST.get('a5f_cigar_number')
	if request.POST.get('a5f_cigar_type') == "1":
		a5_obj.a5f_father_smoke_pipes = True
	else:
		a5_obj.a5f_father_smoke_pipes = False
	a5_obj.a5f_father_smoke_frequency = request.POST.get('a5f_smoking_frequency')
	if request.POST.get('a5f_smoking_presence') == "1":
		a5_obj.a5f_smoke_in_front_of_mother = True
	else:
		a5_obj.a5f_smoke_in_front_of_mother = False	
	###
	if request.POST.get('a5c_smoking_presence') == "1":
		a5_obj.a5c_colleagues_smoking_status = True
	else:
		a5_obj.a5c_colleagues_smoking_status = False	
	a5_obj.a5c_colleagues_smoke = request.POST.get('a5c_smoker_number')
	a5_obj.a5c_duration_with_smokers_per_day = request.POST.get('a5c_daily_duration')
	a5_obj.a5c_month_duration_with_smokers = request.POST.get('a5c_monthly_duration')
	a5_obj.save()
	return a5_obj							        							        