from django.shortcuts import render, redirect
from django.http import HttpResponse
# from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
import datetime

# Create your views here.
@login_required(login_url='core:login')
def check_form(request):
	form = BPregnancy.objects.get(id=request.session['form_id'])
	form.data_checked_id = request.user.username
	form.date_data_checked = datetime.date.today()
	form.save()
	return process_sectionB1A(request)
	
@login_required(login_url='core:login')
def save_form(request):
	form = BPregnancy.objects.get(id=request.session['form_id'])
	form.is_save_all = True
	form.save()
	return show_sectionB1A(request, request.session['form_id'])

@login_required(login_url='core:login')
def edit_form(request):
	form = BPregnancy.objects.get(id=request.session['form_id'])
	form.is_save_all = False
	form.save()
	request.session['edit_mode'] = True
	section_number = request.POST.get('section_number')	
	if section_number == "2":	
		return process_sectionB1B(request)
	elif section_number == "3":
		return process_sectionB1C(request)
	elif section_number == "4":
		return process_sectionB1D(request)
	elif section_number == "5":
		return process_sectionB1E(request)
	else:
		return process_sectionB1A(request)
	

@login_required(login_url='core:login')
def create_form(request):
	if request.method == "POST":		
		b1_obj = BPregnancy()
		b1_obj.participant_id = request.session['participant_id']	
		b1_obj.interviewer_id = request.POST.get('interviewer_id')
		b1_obj.data_entry_id = request.user.username
		b1_obj.date_admission = request.POST.get('date_admission')
		b1_obj.date_interviewed = request.POST.get('date_interviewed')
		b1_obj.date_data_entered = request.POST.get('date_data_entered')
		b1_obj.save()
		request.session['form_id'] = b1_obj.id
		return process_sectionB1A(request)
	else:
		participant = Participant.objects.get(id=request.session['participant_id'])
		date_admission = participant.date_admission.strftime('%Y-%m-%d')
		staff_list = User.objects.filter(is_staff=False)
		return render(request, 'forms_b/form.html', {'staff_list' : staff_list, 'context' : 'create', 'participant' : participant, 'date_admission' : date_admission})