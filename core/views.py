from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from forms_a.models import *
from forms_c.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash


@login_required(login_url='core:login')
def create_participant(request):
	puskesmas_id = request.POST.get('puskesmas')
	number_of_people = Participant.objects.filter(puskesmas_id=puskesmas_id).count()
	puskesmas_obj = Puskesmas.objects.get(id=puskesmas_id)
	participant_obj = Participant()
	participant_obj.name = request.POST.get('participant_name')
	participant_obj.date_admission = request.POST.get('date_admission')
	participant_obj.participant_id =  puskesmas_obj.puskesmas_id+format_number(number_of_people+1)
	participant_obj.puskesmas_id = puskesmas_id
	participant_obj.save()
	return home(request)

def format_number(number):
	if number < 10:
		return "00" + str(number)
	elif number < 100:
		return "0" + str(number)
	else:
		return str(number)			

@login_required(login_url='core:login')
def home(request):
	participants = Participant.objects.all()
	puskesmas_list = Puskesmas.objects.all()
	return render(request, 'core/home.html', {'participants' : participants, 'puskesmas_list' : puskesmas_list})

@login_required(login_url='core:login')
def forms(request):
	request.session['participant_id'] = request.POST.get('participant_id')
	participant = Participant.objects.get(id=request.POST.get('participant_id'))
	date_admission = participant.date_admission.strftime('%Y-%m-%d')
	return render(request, 'core/forms.html', {'participant' : participant, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def form_a(request):
	participant = Participant.objects.get(id=request.session['participant_id'])
	forms = ABaseLine.objects.filter(participant_id=request.session['participant_id'])
	date_admission = participant.date_admission.strftime('%Y-%m-%d')
	return render(request, 'core/form_a.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def form_c(request):	
	participant = Participant.objects.get(id=request.session['participant_id'])
	forms = CBirth.objects.filter(participant_id=request.session['participant_id'])
	date_admission = participant.date_admission.strftime('%Y-%m-%d')
	return render(request, 'core/forms_c.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})