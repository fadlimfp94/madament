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
	return None


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
	return None

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
	return None

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
	return None

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
	return None

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
	return None

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
	return None	