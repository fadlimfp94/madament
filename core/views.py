from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from .models import *

## Fadli
from forms_a.models import *
from forms_d.models import *
##

##GAMA
from forms_b1.models import *
from forms_b2.models import *
from forms_b3.models import *
from forms_c.models import *
##

@login_required(login_url='core:login')
def home(request):
	return redirect('/participant')

@login_required(login_url='core:login')
def summary(request):
	if request.user.is_staff:
		participants = Participant.objects.all()
		summary_list = []
		number_of_completed_participant = 0

		###### filling summary_list ######
		for participant in participants:
			### form A ####
			try:
				form_a = ABaseLine.objects.get(participant=participant)
				if form_a.data_checked_id != None and form_a.data_checked_id != "":
					form_a_status = "3"
				elif form_a.is_save_all:
					form_a_status = "2"
				else:
					form_a_status = "1"
			except:
				form_a_status = ""
			####

			### form B1 ####
			try:
				form_b1 = B1Pregnancy.objects.get(participant=participant)
				if form_b1.data_checked_id != None and form_b1.data_checked_id != "":
					form_b1_status = "3"
				elif form_b1.is_save_all:
					form_b1_status = "2"
				else:
					form_b1_status = "1"	
			except:
				form_b1_status = ""
			####

			### form B2 ####
			try:
				form_b2 = B2Pregnancy.objects.get(participant=participant)
				if form_b2.data_checked_id != None and form_b2.data_checked_id != "":
					form_b2_status = "3"
				elif form_b2.is_save_all:
					form_b2_status = "2"
				else:
					form_b2_status = "1"	
			except:
				form_b2_status = ""
			####

			### form B3 ####
			try:
				form_b3 = B3Pregnancy.objects.get(participant=participant)
				if form_b3.data_checked_id != None and form_b3.data_checked_id != "":
					form_b3_status = "3"
				elif form_b3.is_save_all:
					form_b3_status = "2"
				else:
					form_b3_status = "1"	
			except:
				form_b3_status = ""
			####

			### form C ####
			form_c_all_complete = True
			try:
				form_c_list = CBirth.objects.filter(participant=participant)
				form_c_status = ""
				for form_c in form_c_list:
					if form_c.data_checked_id != None and form_c.data_checked_id != "":
						form_c_status = form_c_status + form_c.child_name + " - 3 | "
					elif form_c.is_save_all:
						form_c_status = form_c_status + form_c.child_name + " - 2 | "
						form_c_all_complete = False
					else:
						form_c_status = form_c_status + form_c.child_name + " - 1 | "
						form_c_all_complete = False	
				form_c_status = form_c_status[:-3]
			except:
				form_c_status = ""
				form_c_all_complete = False
			####

			### form D1 ####
			form_d1_all_complete = True
			try:
				form_d1_list = DInfant.objects.filter(participant=participant)
				form_d1_status = ""
				for form_d1 in form_d1_list:
					if form_d1.data_checked_id != None and form_d1.data_checked_id != "":
						form_d1_status = form_d1_status + form_d1.child_name + " - 3 | "
					elif form_d1.is_save_all:
						form_d1_status = form_d1_status + form_d1.child_name + " - 2 | "
						form_d1_all_complete = False
					else:
						form_d1_status = form_d1_status + form_d1.child_name + " - 1 | "
						form_d1_all_complete = False
				form_d1_status = form_d1_status[:-3]
			except:
				form_d1_status = ""
				form_d1_all_complete = False
			####

			### form D2 ####
			form_d2_all_complete = True
			try:
				form_d2_list = DInfant2.objects.filter(participant=participant)
				form_d2_status = ""
				for form_d2 in form_d2_list:
					if form_d2.data_checked_id != None and form_d2.data_checked_id != "":
						form_d2_status = form_d2_status + form_d2.child_name + " - 3 | "
					elif form_d2.is_save_all:
						form_d2_status = form_d2_status + form_d2.child_name + " - 2 | "
						form_d2_all_complete = False
					else:
						form_d2_status = form_d2_status + form_d2.child_name + " - 1 | "
						form_d2_all_complete = False	
				form_d2_status = form_d2_status[:-3]
			except:
				form_d2_status = ""
				form_d2_all_complete = False
			####

			### form D3 ####
			form_d3_all_complete = True
			try:
				form_d3_list = DInfant3.objects.filter(participant=participant)
				form_d3_status = ""
				for form_d3 in form_d3_list:
					if form_d3.data_checked_id != None and form_d3.data_checked_id != "":
						form_d3_status = form_d3_status + form_d3.child_name + " - 3 | "
					elif form_d3.is_save_all:
						form_d3_status = form_d3_status + form_d3.child_name + " - 2 | "
						form_d3_all_complete = False
					else:
						form_d3_status = form_d3_status + form_d3.child_name + " - 1 | "
						form_d3_all_complete = False
				form_d3_status = form_d3_status[:-3]
			except:
				form_d3_status = ""
				form_d3_all_complete = False
			####

			### form D4 ####
			form_d4_all_complete = True
			try:
				form_d4_list = DInfant4.objects.filter(participant=participant)
				form_d4_status = ""
				for form_d4 in form_d4_list:
					if form_d4.data_checked_id != None and form_d4.data_checked_id != "":
						form_d4_status = form_d4_status + form_d4.child_name + " - 3 | "
					elif form_d4.is_save_all:
						form_d4_status = form_d4_status + form_d4.child_name + " - 2 | "
						form_d4_all_complete = False
					else:
						form_d4_status = form_d4_status + form_d4.child_name + " - 1 | "
						form_d4_all_complete = False	
				form_d4_status = form_d4_status[:-3]
			except:
				form_d4_status = ""
				form_d4_all_complete = False
			####

			if form_a_status == "3" and form_b1_status == "3" and form_b2_status == "3" and form_c_all_complete and form_d1_all_complete and form_d2_all_complete and form_d3_all_complete and form_d4_all_complete:
				number_of_completed_participant = number_of_completed_participant + 1

			summary_list.append([participant.participant_id, participant.name, form_a_status, form_b1_status, form_b2_status, form_b3_status, form_c_status, form_d1_status, form_d2_status, form_d3_status, form_d4_status, participant.id])	
		
		###### end of filling summary_list ######

		return render(request, 'core/summary.html', {'summary_list' : summary_list, 'number_of_completed_participant' : number_of_completed_participant})
	
	else:
		return home(request)


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

### UNUSED SINCE EDIT PARTICIPANT IS NOT IMPLEMENTED 
@login_required(login_url='core:login')
def edit_participant(request, participant_id):
	participant_obj = Participant.objects.get(id=participant_id)
	participant_obj.name = request.POST.get('participant_name_edit')
	participant_obj.date_admission = request.POST.get('participant_date_edit')
	participant_obj.edited_by = request.user.username
	participant_obj.save()
	return home(request)
###


def format_number(number):
	if number < 10:
		return "00" + str(number)
	elif number < 100:
		return "0" + str(number)
	else:
		return str(number)			

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
	#request.session['participant_id'] = participant_id
	participant = Participant.objects.get(id=participant_id)
	date_admission = participant.date_admission
	return render(request, 'core/forms.html', {'participant' : participant, 'date_admission' : date_admission})

##################################
# form fadli
@login_required(login_url='core:login')
def form_a(request, participant_id):
	participant = Participant.objects.get(id=participant_id)
	forms = ABaseLine.objects.filter(participant_id=participant_id)
	date_admission = participant.date_admission
	return render(request, 'core/form_a.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def form_d(request, participant_id, visiting_id):
	participant = Participant.objects.get(id=participant_id)
	child_list = Child.objects.filter(mother=participant)
	forms = None
	visiting_number = ""
	if visiting_id == "1":
		forms = DInfant.objects.filter(participant_id=participant_id)
		visiting_number = "First"
	elif visiting_id == "2":
		forms = DInfant2.objects.filter(participant_id=participant_id)
		visiting_number = "Second"
	elif visiting_id == "3":
		forms = DInfant3.objects.filter(participant_id=participant_id)
		visiting_number = "Third"
	elif visiting_id == "4":
		forms = DInfant4.objects.filter(participant_id=participant_id)
		visiting_number = "Fourth"
	else:
		raise ValueError("Oops! We can't find the page you are looking for")	
	date_admission = participant.date_admission
	return render(request, 'core/form_d.html', {'child_list' : child_list, 'visiting_number' : visiting_number,'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})


##################################

# form gama
@login_required(login_url='core:login')
def form_c(request, participant_id):	
	participant = Participant.objects.get(id=participant_id)
	forms = CBirth.objects.filter(participant_id=participant_id)
	date_admission = participant.date_admission
	return render(request, 'core/form_c.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def form_b1(request, participant_id):
	participant = Participant.objects.get(id=participant_id)
	forms = B1Pregnancy.objects.filter(participant_id=participant_id)
	date_admission = participant.date_admission
	return render(request, 'core/form_b1.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def form_b2(request, participant_id):
	participant = Participant.objects.get(id=participant_id)
	forms = B2Pregnancy.objects.filter(participant_id=participant_id)
	date_admission = participant.date_admission
	return render(request, 'core/form_b2.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def form_b3(request, participant_id):
	participant = Participant.objects.get(id=participant_id)
	forms = B3Pregnancy.objects.filter(participant_id=participant_id)
	date_admission = participant.date_admission
	return render(request, 'core/form_b3.html', {'participant' : participant, 'forms' : forms, 'date_admission' : date_admission})

	##################################