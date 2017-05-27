from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from forms_a.models import *
from forms_d.models import *
#from forms_b1.models import *	
#from forms_c.models import *

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
	return redirect('/participant')

@login_required(login_url='core:login')
def participant_list(request):
	participants = Participant.objects.all()
	puskesmas_list = Puskesmas.objects.all()
	number_of_participants_list = []
	for puskesmas in puskesmas_list:
		number_of_participants_list.append(puskesmas.name + ": " + str(Participant.objects.filter(puskesmas=puskesmas).count()))	
	return render(request, 'core/home.html', {'number_of_participants_list' : number_of_participants_list,'participants' : participants, 'puskesmas_list' : puskesmas_list})


@login_required(login_url='core:login')
def children(request):
	request.session['participant_id'] = request.POST.get('participant_id')
	participant = Participant.objects.get(id=request.POST.get('participant_id'))
	children = Children.objects.get(mother_id=request.POST.get('participant_id'))
	date_admission = participant.date_admission.strftime('%Y-%m-%d')
	return render(request, 'core/children.html', {'children' : children,'participant' : participant, 'date_admission' : date_admission})

#KERJAKAN INI
@login_required(login_url='core:login')
def add_children(request):
	puskesmas_id = request.POST.get('puskesmas')
	number_of_people = Participant.objects.filter(puskesmas_id=puskesmas_id).count()
	participant = Participant.objects.get(id=request.session('participant_id'))
	children_obj = Children.objects.get(mother_id=request.session['participant_id'])
	child_obj = Children()
	child_obj.first_name = request.POST.get('first_name')
	child_obj.surname = request.POST.get('surname')
	child_obj.date_of_birth = request.POST.get('date_of_birth')
	child_obj.ur_number =  puskesmas_obj.puskesmas_id+format_number(number_of_people+1)
	child_obj.save()
	return children(request)

	request.session['participant_id'] = request.POST.get('participant_id')
	participant = Participant.objects.get(id=request.POST.get('participant_id'))
	children = Children.objects.get(mother_id=request.POST.get('participant_id'))
	date_admission = participant.date_admission.strftime('%Y-%m-%d')
	return render(request, 'core/children.html', {'children' : children,'participant' : participant, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def forms(request, participant_id):
	request.session['participant_id'] = participant_id
	participant = Participant.objects.get(id=participant_id)
	date_admission = participant.date_admission.strftime('%Y-%m-%d')
	return render(request, 'core/forms.html', {'participant' : participant, 'date_admission' : date_admission})


# form fadli
@login_required(login_url='core:login')
def form_a(request, participant_id):
	participant = Participant.objects.get(id=request.session['participant_id'])
	forms = ABaseLine.objects.filter(participant_id=request.session['participant_id'])
	date_admission = participant.date_admission.strftime('%Y-%m-%d')
	return render(request, 'core/form_a.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def form_d1(request, participant_id):
	participant = Participant.objects.get(id=request.session['participant_id'])
	forms = DInfant.objects.filter(participant_id=request.session['participant_id'])
	date_admission = participant.date_admission.strftime('%Y-%m-%d')
	return render(request, 'core/form_d.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def form_d2(request, participant_id):
	participant = Participant.objects.get(id=request.session['participant_id'])
	forms = DInfant2.objects.filter(participant_id=request.session['participant_id'])
	date_admission = participant.date_admission.strftime('%Y-%m-%d')
	return render(request, 'core/form_d.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def form_d3(request, participant_id):
	participant = Participant.objects.get(id=request.session['participant_id'])
	forms = DInfant3.objects.filter(participant_id=request.session['participant_id'])
	date_admission = participant.date_admission.strftime('%Y-%m-%d')
	return render(request, 'core/form_d.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def form_d4(request, participant_id):
	participant = Participant.objects.get(id=request.session['participant_id'])
	forms = DInfant4.objects.filter(participant_id=request.session['participant_id'])
	date_admission = participant.date_admission.strftime('%Y-%m-%d')
	return render(request, 'core/form_d.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})



##################################

# form gama
@login_required(login_url='core:login')
def form_c(request, participant_id):	
	participant = Participant.objects.get(id=request.session['participant_id'])
	forms = CBirth.objects.filter(participant_id=request.session['participant_id'])
	date_admission = participant.date_admission.strftime('%Y-%m-%d')
	return render(request, 'core/form_c.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def form_b1(request, participant_id):
	participant = Participant.objects.get(id=request.session['participant_id'])
	forms = BPregnancy.objects.filter(participant_id=request.session['participant_id'])
	date_admission = participant.date_admission.strftime('%Y-%m-%d')
	return render(request, 'core/form_b1.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def form_b2(request, participant_id):
	participant = Participant.objects.get(id=request.session['participant_id'])
	forms = BPregnancy.objects.filter(participant_id=request.session['participant_id'])
	date_admission = participant.date_admission.strftime('%Y-%m-%d')
	return render(request, 'core/form_b1.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def form_b3(request, participant_id):
	participant = Participant.objects.get(id=request.session['participant_id'])
	forms = BPregnancy.objects.filter(participant_id=request.session['participant_id'])
	date_admission = participant.date_admission.strftime('%Y-%m-%d')
	return render(request, 'core/form_b1.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})