from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from forms_a.models import *
from forms_d.models import *


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
	participant_obj.created_by = request.user.username
	participant_obj.edited_by = request.user.username
	participant_obj.save()
	return home(request)

@login_required(login_url='core:login')
def edit_participant(request, participant_id):
	participant_obj = Participant.objects.get(id=participant_id)
	participant_obj.name = request.POST.get('participant_name_edit')
	participant_obj.date_admission = request.POST.get('participant_date_edit')
	participant_obj.edited_by = request.user.username
	participant_obj.save()
	print "tes"
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
def redirect_to_forms(request, participant_id):
	return redirect('/participant/'+str(participant_id)+'/')	

@login_required(login_url='core:login')
def participant_list(request):
	participants = Participant.objects.all()
	puskesmas_list = Puskesmas.objects.all()
	number_of_participants_list = []
	for puskesmas in puskesmas_list:
		number_of_participants_list.append(puskesmas.name + ": " + str(Participant.objects.filter(puskesmas=puskesmas).count()))	
	return render(request, 'core/home.html', {'number_of_participants_list' : number_of_participants_list,'participants' : participants, 'puskesmas_list' : puskesmas_list})


@login_required(login_url='core:login')
def forms(request, participant_id):
	request.session['participant_id'] = participant_id
	participant = Participant.objects.get(id=participant_id)
	date_admission = participant.date_admission
	return render(request, 'core/forms.html', {'participant' : participant, 'date_admission' : date_admission})

##################################
# form fadli
@login_required(login_url='core:login')
def form_a(request, participant_id):
	participant = Participant.objects.get(id=request.session['participant_id'])
	forms = ABaseLine.objects.filter(participant_id=request.session['participant_id'])
	date_admission = participant.date_admission
	return render(request, 'core/form_a.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def form_d(request, participant_id, visiting_id):
	participant = Participant.objects.get(id=request.session['participant_id'])
	forms = None
	visiting_number = ""
	if visiting_id == "1":
		forms = DInfant.objects.filter(participant_id=request.session['participant_id'])
		visiting_number = "First"
	elif visiting_id == "2":
		forms = DInfant2.objects.filter(participant_id=request.session['participant_id'])
		visiting_number = "Second"
	elif visiting_id == "3":
		forms = DInfant3.objects.filter(participant_id=request.session['participant_id'])
		visiting_number = "Third"
	elif visiting_id == "4":
		forms = DInfant4.objects.filter(participant_id=request.session['participant_id'])
		visiting_number = "Fourth"
	else:
		raise ValueError("Oops! We can't find the page you are looking for")	
	date_admission = participant.date_admission
	return render(request, 'core/form_d.html', {'visiting_number' : visiting_number,'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})


##################################

# form gama