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
def check_form(request, participant_id, form_id):
	form = B2Pregnancy.objects.get(id=int(form_id))
	if request.user.is_staff and form.is_save_all:
		form.data_checked_id = request.user.username
		form.date_data_checked = datetime.date.today()
		form.save()
	return process_sectionB2A(request, participant_id, form_id)
	
@login_required(login_url='core:login')
def save_form(request, participant_id, form_id):
	form = B2Pregnancy.objects.get(id=int(form_id))
	form.is_save_all = True
	form.save()
	return process_sectionB2A(request, participant_id, form_id)

@login_required(login_url='core:login')
def edit_form(request, participant_id, form_id):
	form = B2Pregnancy.objects.get(id=int(form_id))
	if request.user.is_staff and (form.data_checked_id == "" or form.data_checked_id == None):
		form.is_save_all = False
		form.save()
		request.session['edit_mode'] = True
	section_number = request.POST.get('section_number')	
	if section_number == "2":	
		return process_sectionB2B(request, participant_id, form_id)
	elif section_number == "3":
		return process_sectionB2C(request, participant_id, form_id)
	elif section_number == "4":
		return process_sectionB2D(request, participant_id, form_id)
	elif section_number == "5":
		return process_sectionB2E(request, participant_id, form_id)
	elif section_number == "6":
		return process_sectionB2F(request, participant_id, form_id)
	else:
		return process_sectionB2A(request, participant_id, form_id)
	

@login_required(login_url='core:login')
def create_form(request, participant_id):
	if request.method == "POST":		
		b1_obj = B2Pregnancy()
		b1_obj.participant_id = participant_id
		b1_obj.interviewer_id = request.POST.get('interviewer_id')
		b1_obj.data_entry_id = request.user.username
		b1_obj.date_admission = request.POST.get('date_admission')
		b1_obj.date_interviewed = request.POST.get('date_interviewed')
		b1_obj.date_data_entered = request.POST.get('date_data_entered')
		b1_obj.save()
		return process_form(request, participant_id, b1_obj.id)
	else:
		print "masuk kesini form_b2"
		participant = Participant.objects.get(id=int(participant_id))
		date_admission = participant.date_admission.__str__()
		staff_list = User.objects.filter(is_staff=False)
		return render(request, 'forms_b2/form.html', {'staff_list' : staff_list, 'context' : 'create_new_form', 'participant' : participant, 'date_admission' : date_admission})

@login_required(login_url='core:login')
def process_form(request, participant_id, form_id):
	print 0
	return redirect('/participant/'+str(participant_id)+'/form_b2/'+str(form_id)+'/sectionB2A')

@login_required(login_url='core:login')
def process_sectionB2A(request, participant_id, form_id):
	
	b1_form_obj = B2Pregnancy.objects.get(id=int(form_id))
	try:
		b1_obj = B2MedicalData.objects.get(b1_form=b1_form_obj)
		print "masuk ke update_section1"
		return update_sectionB2A(request, participant_id, form_id)	
	except:
		print "masuk ke create_section1"
		return create_sectionB2A(request, participant_id, form_id)

@login_required(login_url='core:login')
def create_sectionB2A(request, participant_id, form_id):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		b1_form_obj = B2Pregnancy.objects.get(id=int(form_id))
		b1_obj = B2MedicalData()
		b1_obj.b1_form = b1_form_obj
		b1_obj.participant_id = b1_form_obj.participant.participant_id
		b1_obj.data_entry_id = request.user.username
		b1_obj.created_time = datetime.datetime.now()
		b1_obj = save_sectionB2A(b1_obj, request, participant_id, form_id)
		print "masuk ke show section true"
		return show_sectionB2A(request,participant_id,form_id, True)	
	else:
		print "masuk ke show section false"
		return show_sectionB2A(request, participant_id,form_id,False)

@login_required(login_url='core:login')
def update_sectionB2A(request, participant_id, form_id):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		b1_obj = B2MedicalData.objects.get(b1_form_id=int(form_id))
		b1_obj = save_sectionB2A(b1_obj, request, participant_id, form_id)
		print "masuk ke show section yang diupdate true"
		return show_sectionB2A(request,participant_id ,form_id,True)	
	else:
		print "masuk ke show section1 yang diupdate false"
		return show_sectionB2A(request,participant_id ,form_id,False)

@login_required(login_url='core:login')
def show_sectionB2A(request,participant_id,form_id, is_save):
	form = B2Pregnancy.objects.get(id=int(form_id))
	participant = Participant.objects.get(id=int(participant_id))
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all	
	date_interviewed = form.date_interviewed
	date_data_entered = form.date_data_entered
	date_admission = form.date_admission
	role = ''
	if not request.user.is_staff:
		role = 'staff'
	try:
		b1_obj = B2MedicalData.objects.get(b1_form_id=form.id) 			
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked
			if is_save:
				return render(request, 'forms_b2/sectionB2A.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj,  'date_data_checked' : date_data_checked})
			else:
				print 'b'
				return render(request, 'forms_b2/sectionB2A.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj, 'date_data_checked' : date_data_checked})
		else:
			print 'c'
			if is_save:	
				print 'masuk ke yang is_save = true '
				return render(request, 'forms_b2/sectionB2A.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj })
			else:
				print 'masuk ke yang is_save = false'
				return render(request, 'forms_b2/sectionB2A.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj })	
	except:
		print "masuk ke except yang form B1"
		return render(request, 'forms_b2/sectionB2A.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

def save_sectionB2A(b1_obj, request, participant_id, form_id):
	
	b1_obj.updated_time = datetime.datetime.now()
	b1_obj.data_updated_id = request.user.username
	b1_obj.b1m_weight = request.POST.get('b1m_weight')
	b1_obj.b1m_fundal = request.POST.get('b1m_fundal')
	b1_obj.b1m_systolic1st = request.POST.get('b1m_systolic1st')
	b1_obj.b1m_systolic2nd = request.POST.get('b1m_systolic2nd')
	b1_obj.b1m_diastolic1st = request.POST.get('b1m_diastolic1st')
	b1_obj.b1m_diastolic2nd = request.POST.get('b1m_diastolic2nd')
	b1_obj.b1m_complication = request.POST.get('b1m_complication')

	if request.POST.get('b1m_hypertensioncom') == 'on':
		b1_obj.b1m_hypertensioncom = True
	else:
		b1_obj.b1m_hypertensioncom = False

	if request.POST.get('b1m_visualcom') == 'on':
		b1_obj.b1m_visualcom = True
	else:
		b1_obj.b1m_visualcom = False

	if request.POST.get('b1m_consciousnesscom') == 'on':
		b1_obj.b1m_consciousnesscom = True
	else:
		b1_obj.b1m_consciousnesscom = False

	if request.POST.get('b1m_seizurecom') == 'on':
		b1_obj.b1m_seizurecom = True
	else:
		b1_obj.b1m_seizurecom = False

	if request.POST.get('b1m_diabetescom') == 'on':
		b1_obj.b1m_diabetescom = True
	else:
		b1_obj.b1m_diabetescom = False

	if request.POST.get('b1m_eclampsiacom') == 'on':
		b1_obj.b1m_eclampsiacom = True
	else:
		b1_obj.b1m_eclampsiacom = False

	if request.POST.get('b1m_laborcom') == 'on':
		b1_obj.b1m_laborcom = True
	else:
		b1_obj.b1m_laborcom = False

	if request.POST.get('b1m_hypremesiscom') == 'on':
		b1_obj.b1m_hypremesiscom = True
	else:
		b1_obj.b1m_hypremesiscom = False
	 
	if request.POST.get('b1m_tbcom') == 'on':
		b1_obj.b1m_tbcom = True
	else:
		b1_obj.b1m_tbcom = False

	if request.POST.get('b1m_hivcom') == 'on':
		b1_obj.b1m_hivcom = True
	else:
		b1_obj.b1m_hivcom = False

	if request.POST.get('b1m_urinarycom') == 'on':
		b1_obj.b1m_urinarycom = True
	else:
		b1_obj.b1m_urinarycom = False

	if request.POST.get('b1m_fevercom') == 'on':
		b1_obj.b1m_fevercom = True
	else:
		b1_obj.b1m_fevercom = False

	if request.POST.get('b1m_respiratorycom') == 'on':
		b1_obj.b1m_respiratorycom = True
	else:
		b1_obj.b1m_respiratorycom = False

	if request.POST.get('b1m_pulmonarycom') == 'on':
		b1_obj.b1m_pulmonarycom = True
	else:
		b1_obj.b1m_pulmonarycom = False

	if request.POST.get('b1m_chroniccom') == 'on':
		b1_obj.b1m_chroniccom = True
	else:
		b1_obj.b1m_chroniccom = False

	if request.POST.get('b1m_gastroentetriscom') == 'on':
		b1_obj.b1m_gastroentetriscom = True
	else:
		b1_obj.b1m_gastroentetriscom = False	 
	 
	b1_obj.b1m_other = request.POST.get('b1m_other')
	b1_obj.b1m_notes = request.POST.get('b1m_notes')
	b1_obj.save()
	return b1_obj

@login_required(login_url='core:login')
def process_sectionB2B(request, participant_id,form_id):
	# if request.POST.get('form_id'):
	# 	int(form_id) = request.POST.get('form_id')
	b1_form_obj = B2Pregnancy.objects.get(id=int(form_id))
	
	try:
		b1_obj = B2UltrasoundScanResults.objects.get(b1_form=b1_form_obj)
		print b1_obj
		print "masuk ke update_section1"
		return update_sectionB2B(request, participant_id, form_id)	
	except:
		print "masuk ke create_section1"
		return create_sectionB2B(request, participant_id, form_id)

@login_required(login_url='core:login')
def create_sectionB2B(request, participant_id, form_id):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		b1_form_obj = B2Pregnancy.objects.get(id=int(form_id))
		b1_obj = B2UltrasoundScanResults()
		b1_obj.b1_form = b1_form_obj
		b1_obj.participant_id = b1_form_obj.participant.participant_id
		b1_obj.data_entry_id = request.user.username
		b1_obj.created_time = datetime.datetime.now()
		b1_obj = save_sectionB2B(b1_obj, request, participant_id, form_id)
		print "masuk ke show section true"
		return show_sectionB2B(request, participant_id, form_id, True)	
	else:
		print "masuk ke show section false"
		return show_sectionB2B(request, participant_id, form_id, False)

@login_required(login_url='core:login')
def update_sectionB2B(request, participant_id, form_id):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		b1_obj = B2UltrasoundScanResults.objects.get(b1_form_id=int(form_id))
		b1_obj = save_sectionB2B(b1_obj, request, participant_id, form_id)
		print "masuk ke show section yang diupdate true"
		return show_sectionB2B(request, participant_id, form_id, True)	
	else:
		print "masuk ke show section1 yang diupdate false"
		return show_sectionB2B(request, participant_id, form_id, False)

@login_required(login_url='core:login')
def show_sectionB2B(request, participant_id, form_id, is_save):
	form = B2Pregnancy.objects.get(id=int(form_id))
	participant = Participant.objects.get(id=int(participant_id))
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all	
	date_interviewed = form.date_interviewed
	date_data_entered = form.date_data_entered
	date_admission = form.date_admission
	role = ''
	if not request.user.is_staff:
		role = 'staff'
	try:

		b1_obj = B2UltrasoundScanResults.objects.get(b1_form_id=form.id)
		#date_exam = b1_obj.b2m_date_exam
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked
			if is_save:
				return render(request, 'forms_b2/sectionB2B.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj,  'date_data_checked' : date_data_checked})
			else:
				print 'b'
				return render(request, 'forms_b2/sectionB2B.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj, 'date_data_checked' : date_data_checked})
		else:
			print 'c'
			if is_save:	
				print 'masuk ke yang is_save = true '
				return render(request, 'forms_b2/sectionB2B.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj })
			else:
				print 'masuk ke yang is_save = false'
				return render(request, 'forms_b2/sectionB2B.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj})	

	except:
		print "masuk ke except yang form B1"
		return render(request, 'forms_b2/sectionB2B.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

def save_sectionB2B(b1_obj, request, participant_id, form_id):
	b1_form =  models.ForeignKey(B2Pregnancy, on_delete=models.PROTECT)
	
	b1_obj.updated_time = datetime.datetime.now()
	b1_obj.data_updated_id = request.user.username
	b1_obj.b2m_date_exam = request.POST.get('b2m_date_exam')	
	b1_obj.b2m_gestat_age = request.POST.get('b2m_gestat_age')
	b1_obj.b2m_hc = request.POST.get('b2m_hc')
	b1_obj.b2m_ac = request.POST.get('b2m_ac')
	b1_obj.b2m_bd = request.POST.get('b2m_bd')
	b1_obj.b2m_fl = request.POST.get('b2m_fl')
	b1_obj.b2m_di = request.POST.get('b2m_di')
	b1_obj.b2m_conanomaly = request.POST.get('b2m_conanomaly')
	b1_obj.b2m_conanomaly_specify = request.POST.get('b2m_conanomaly_specify')
	b1_obj.b2m_SVDoppler = request.POST.get('b2m_SVDoppler')
	b1_obj.b2m_DVDoppler = request.POST.get('b2m_DVDoppler')
	b1_obj.b2m_sd_ratio = request.POST.get('b2m_sd_ratio')
	b1_obj.b2m_rimca = request.POST.get('b2m_rimca')
	b1_obj.b2m_amnion = request.POST.get('b2m_amnion')
	b1_obj.b2m_notes = request.POST.get('b2m_notes')
	b1_obj.save()
	return b1_obj

@login_required(login_url='core:login')
def process_sectionB2C(request, participant_id, form_id):
	# if request.POST.get('form_id'):
	# 	int(form_id) = request.POST.get('form_id')
	b1_form_obj = B2Pregnancy.objects.get(id=int(form_id))
	print b1_form_obj
	try:
		b1_obj = B2LaboratoryTest.objects.get(b1_form=b1_form_obj)
		print b1_obj
		print "masuk ke update_section1"
		return update_sectionB2C(request, participant_id, form_id)	
	except:
		print "masuk ke create_section1"
		return create_sectionB2C(request, participant_id, form_id)

@login_required(login_url='core:login')
def create_sectionB2C(request, participant_id, form_id):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		b1_form_obj = B2Pregnancy.objects.get(id=int(form_id))
		b1_obj = B2LaboratoryTest()
		b1_obj.b1_form = b1_form_obj		
		b1_obj.participant_id = b1_form_obj.participant.participant_id
		b1_obj.data_entry_id = request.user.username
		b1_obj.created_time = datetime.datetime.now()
		b1_obj = save_sectionB2C(b1_obj, request, participant_id, form_id)
		print "masuk ke show section true"
		return show_sectionB2C(request, participant_id, form_id, True)	
	else:
		print "masuk ke show section false"
		return show_sectionB2C(request, participant_id, form_id, False)

@login_required(login_url='core:login')
def update_sectionB2C(request, participant_id, form_id):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		b1_obj = B2LaboratoryTest.objects.get(b1_form_id=int(form_id))
		b1_obj = save_sectionB2C(b1_obj, request, participant_id, form_id)
		print "masuk ke show section yang diupdate true"
		return show_sectionB2C(request, participant_id, form_id, True)	
	else:
		print "masuk ke show section1 yang diupdate false"
		return show_sectionB2C(request, participant_id, form_id, False)

@login_required(login_url='core:login')
def show_sectionB2C(request, participant_id, form_id, is_save):
	form = B2Pregnancy.objects.get(id=int(form_id))
	participant = Participant.objects.get(id=int(participant_id))
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all	
	date_interviewed = form.date_interviewed
	date_data_entered = form.date_data_entered
	date_admission = form.date_admission

	role = ''
	if not request.user.is_staff:
		role = 'staff'
	try:
		b1_obj = B2LaboratoryTest.objects.get(b1_form_id=form.id)	
		
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked
			if is_save:
				return render(request, 'forms_b2/sectionB2C.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj,  'date_data_checked' : date_data_checked})
			else:
				print 'b'
				return render(request, 'forms_b2/sectionB2C.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj, 'date_data_checked' : date_data_checked })
		else:
			print 'c'
			if is_save:	
				print 'masuk ke yang is_save = true '
				return render(request, 'forms_b2/sectionB2C.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj})
			else:
				print 'masuk ke yang is_save = false'
				return render(request, 'forms_b2/sectionB2C.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj})	
	except:
		print "masuk ke except yang form B1"
		return render(request, 'forms_b2/sectionB2C.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})


def save_sectionB2C(b1_obj, request, participant_id, form_id):
	b1_form =  models.ForeignKey(B2Pregnancy, on_delete=models.PROTECT)

	# b1_obj.b4m_household_smoker = request.POST.get('b4m_household_smoker')

	#DATE
	
	b1_obj.updated_time = datetime.datetime.now()
	b1_obj.data_updated_id = request.user.username
	b1_obj.b3m_date_urin =  request.POST.get('b3m_date_urin')
	b1_obj.b3m_proteinuria = request.POST.get('b3m_proteinuria')
	b1_obj.b3m_blood_test = request.POST.get('b3m_blood_test')
	b1_obj.b3m_date_blood = request.POST.get('b3m_date_blood')
	b1_obj.b3m_hb = request.POST.get('b3m_hb')
	b1_obj.b3m_rbc = request.POST.get('b3m_rbc')
	b1_obj.b3m_wbc = request.POST.get('b3m_wbc')
	b1_obj.b3m_thrombocyte = request.POST.get('b3m_thrombocyte')
	b1_obj.b3m_SGOT =  request.POST.get('b3m_SGOT')
	b1_obj.b3m_SGPT = request.POST.get('b3m_SGPT')
	b1_obj.b3m_ureum = request.POST.get('b3m_ureum')
	b1_obj.b3m_creatinine = request.POST.get('b3m_creatinine')
	b1_obj.b3m_hiv_test = request.POST.get('b3m_hiv_test')
	b1_obj.b3m_hiv_date = request.POST.get('b3m_hiv_date')
	b1_obj.b3m_hiv_status = request.POST.get('b3m_hiv_status')
	b1_obj.b3m_hepB_test = request.POST.get('b3m_hepB_test')
	b1_obj.b3m_hepB_date = request.POST.get('b3m_hepB_date')
	b1_obj.b3m_hepB_status = request.POST.get('b3m_hepB_status')
	b1_obj.b3m_torch_test = request.POST.get('b3m_torch_test')
	b1_obj.b3m_torch_date = request.POST.get('b3m_torch_date')
	b1_obj.b3m_toxo = request.POST.get('b3m_toxo')
	b1_obj.b3m_rubella = request.POST.get('b3m_rubella')
	b1_obj.b3m_cmv = request.POST.get('b3m_cmv')
	b1_obj.b3m_herpes = request.POST.get('b3m_herpes')
	b1_obj.b3m_urin_date = request.POST.get('b3m_urin_date')
	b1_obj.b3m_blood_date = request.POST.get('b3m_blood_date')
	b1_obj.b3m_stool_date = request.POST.get('b3m_stool_date')
	b1_obj.b3m_hair_date = request.POST.get('b3m_hair_date')
	b1_obj.b3m_nail_date = request.POST.get('b3m_nail_date')
	b1_obj.b3m_lung_date = request.POST.get('b3m_lung_date')
	b1_obj.b3m_FVC1st = request.POST.get('b3m_FVC1st')
	b1_obj.b3m_FVC2nd = request.POST.get('b3m_FVC2nd')
	b1_obj.b3m_FVC3rd = request.POST.get('b3m_FVC3rd')
	b1_obj.b3m_FEV11st = request.POST.get('b3m_FEV11st')
	b1_obj.b3m_FEV12nd = request.POST.get('b3m_FEV12nd')
	b1_obj.b3m_FEV13rd = request.POST.get('b3m_FEV13rd')
	b1_obj.b3m_FEV31st = request.POST.get('b3m_FEV31st')
	b1_obj.b3m_FEV32nd = request.POST.get('b3m_FEV32nd')
	b1_obj.b3m_FEV33rd = request.POST.get('b3m_FEV33rd')
	b1_obj.b3m_PEF1st = request.POST.get('b3m_PEF1st')
	b1_obj.b3m_PEF2nd = request.POST.get('b3m_PEF2nd')
	b1_obj.b3m_PEF3rd = request.POST.get('b3m_PEF3rd')
	b1_obj.b3m_FEF25751st = request.POST.get('b3m_FEF25751st')
	b1_obj.b3m_FEF25752nd = request.POST.get('b3m_FEF25752nd')
	b1_obj.b3m_FEF25753rd = request.POST.get('b3m_FEF25753rd')
	b1_obj.b3m_notes = request.POST.get('b3m_notes')

	b1_obj.save()
	return b1_obj


@login_required(login_url='core:login')
def process_sectionB2D(request, participant_id, form_id):
	
	b1_form_obj = B2Pregnancy.objects.get(id=int(form_id))
	try:
		b1_obj = B2CurrentSmookingHabits.objects.get(b1_form=b1_form_obj)
		print "masuk ke update_section1"
		return update_sectionB2D(request, participant_id, form_id)	
	except:
		print "masuk ke create_section1"
		return create_sectionB2D(request, participant_id, form_id)

@login_required(login_url='core:login')
def create_sectionB2D(request, participant_id, form_id):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		b1_form_obj = B2Pregnancy.objects.get(id=int(form_id))
		b1_obj = B2CurrentSmookingHabits()
		b1_obj.b1_form = b1_form_obj
		b1_obj.participant_id = b1_form_obj.participant.participant_id
		b1_obj.data_entry_id = request.user.username
		b1_obj.created_time = datetime.datetime.now()
		b1_obj = save_sectionB2D(b1_obj, request, participant_id, form_id)
		print "masuk ke show section true"
		return show_sectionB2D(request, participant_id, form_id, True)	
	else:
		print "masuk ke show section false"
		return show_sectionB2D(request, participant_id, form_id, False)

@login_required(login_url='core:login')
def update_sectionB2D(request, participant_id, form_id):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		b1_obj = B2CurrentSmookingHabits.objects.get(b1_form_id=int(form_id))
		b1_obj = save_sectionB2D(b1_obj, request, participant_id, form_id)
		print "masuk ke show section yang diupdate true"
		return show_sectionB2D(request, participant_id, form_id, True)	
	else:
		print "masuk ke show section1 yang diupdate false"
		return show_sectionB2D(request, participant_id, form_id, False)

@login_required(login_url='core:login')
def show_sectionB2D(request, participant_id, form_id, is_save):
	form = B2Pregnancy.objects.get(id=int(form_id))
	participant = Participant.objects.get(id=int(participant_id))
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all	
	date_interviewed = form.date_interviewed
	date_data_entered = form.date_data_entered
	date_admission = form.date_admission
	role = ''
	if not request.user.is_staff:
		role = 'staff'
	try:
		b1_obj = B2CurrentSmookingHabits.objects.get(b1_form_id=form.id) 			
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked
			if is_save:
				return render(request, 'forms_b2/sectionB2D.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj,  'date_data_checked' : date_data_checked})
			else:
				print 'b'
				return render(request, 'forms_b2/sectionB2D.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj, 'date_data_checked' : date_data_checked})
		else:
			print 'c'
			if is_save:	
				print 'masuk ke yang is_save = true '
				return render(request, 'forms_b2/sectionB2D.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj})
			else:
				print 'masuk ke yang is_save = false'
				return render(request, 'forms_b2/sectionB2D.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj})	
	except:
		print "masuk ke except yang form B1"
		return render(request, 'forms_b2/sectionB2D.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})


def save_sectionB2D(b1_obj, request, participant_id, form_id):
	b1_form =  models.ForeignKey(B2Pregnancy, on_delete=models.PROTECT)
	
	b1_obj.updated_time = datetime.datetime.now()
	b1_obj.data_updated_id = request.user.username
	b1_obj.b4m_smoking_status = request.POST.get('b4m_smoking_status')
	b1_obj.b4m_quitting_duration = request.POST.get('b4m_quitting_duration')
	b1_obj.b4m_cigar_type = request.POST.get('b4m_cigar_type')
	b1_obj.b4m_cigar_number = request.POST.get('b4m_cigar_number')
	b1_obj.b4m_household_smoker = request.POST.get('b4m_household_smoker')
	b1_obj.b4m_household_smoker_number = request.POST.get('b4m_household_smoker_number')
	b1_obj.b4m_household_total_cigar = request.POST.get('b4m_household_total_cigar')
	b1_obj.b4m_household_presence = request.POST.get('b4m_household_presence')	
	b1_obj.b4f_smoking_status = request.POST.get('b4f_smoking_status')
	b1_obj.b4f_quitting_duration = request.POST.get('b4f_quitting_duration')
	b1_obj.b4f_cigar_number = request.POST.get('b4f_cigar_number')
	b1_obj.b4f_cigar_type = request.POST.get('b4f_cigar_type')
	b1_obj.b4f_smoking_inside_house = request.POST.get('b4f_smoking_inside_house')
	b1_obj.b4f_smoking_presence = request.POST.get('b4f_smoking_presence')	
	b1_obj.b4c_smoking_presence = request.POST.get('b4c_smoking_presence')
	b1_obj.b4c_smoker_number = request.POST.get('b4c_smoker_number')
	b1_obj.b4c_daily_duration = request.POST.get('b4c_daily_duration')	
	b1_obj.b4m_notes = request.POST.get('b4m_notes')	
	b1_obj.save()
	return b1_obj


@login_required(login_url='core:login')
def process_sectionB2E(request, participant_id, form_id):	
	b1_form_obj = B2Pregnancy.objects.get(id=int(form_id))
	try:
		b1_obj = B2PollutanExposure.objects.get(b1_form=b1_form_obj)
		print "masuk ke update_section1"
		return update_sectionB2E(request, participant_id, form_id)	
	except:
		print "masuk ke create_section1"
		return create_sectionB2E(request, participant_id, form_id)

@login_required(login_url='core:login')
def create_sectionB2E(request, participant_id, form_id):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		b1_form_obj = B2Pregnancy.objects.get(id=int(form_id))
		b1_obj = B2PollutanExposure()
		b1_obj.b1_form = b1_form_obj
		b1_obj.participant_id = b1_form_obj.participant.participant_id
		b1_obj.data_entry_id = request.user.username
		b1_obj.created_time = datetime.datetime.now()
		b1_obj = save_sectionB2E(b1_obj, request, participant_id, form_id)
		print "masuk ke show section true"
		return show_sectionB2E(request, participant_id, form_id, True)	
	else:
		print "masuk ke show section false"
		return show_sectionB2E(request, participant_id, form_id, False)

@login_required(login_url='core:login')
def update_sectionB2E(request, participant_id, form_id):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		b1_obj = B2PollutanExposure.objects.get(b1_form_id=int(form_id))
		b1_obj = save_sectionB2E(b1_obj, request, participant_id, form_id)
		print "masuk ke show section yang diupdate true"
		return show_sectionB2E(request, participant_id, form_id, True)	
	else:
		print "masuk ke show section1 yang diupdate false"
		return show_sectionB2E(request, participant_id, form_id, False)

@login_required(login_url='core:login')
def show_sectionB2E(request, participant_id, form_id, is_save):
	form = B2Pregnancy.objects.get(id=int(form_id))
	participant = Participant.objects.get(id=int(participant_id))
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all	
	date_interviewed = form.date_interviewed
	date_data_entered = form.date_data_entered
	date_admission = form.date_admission
	role = ''
	if not request.user.is_staff:
		role = 'staff'
	try:
		b1_obj = B2PollutanExposure.objects.get(b1_form_id=form.id) 			
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked
			if is_save:
				return render(request, 'forms_b2/sectionB2E.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj,  'date_data_checked' : date_data_checked})
			else:
				print 'b'
				return render(request, 'forms_b2/sectionB2E.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj, 'date_data_checked' : date_data_checked})
		else:
			print 'c'
			if is_save:	
				print 'masuk ke yang is_save = true '
				return render(request, 'forms_b2/sectionB2E.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj})
			else:
				print 'masuk ke yang is_save = false'
				return render(request, 'forms_b2/sectionB2E.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj})	
	except:
		print "masuk ke except yang form B1"
		return render(request, 'forms_b2/sectionB2E.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

def save_sectionB2E(b1_obj, request, participant_id, form_id):
	b1_form =  models.ForeignKey(B2Pregnancy, on_delete=models.PROTECT)
	
	b1_obj.updated_time = datetime.datetime.now()
	b1_obj.data_updated_id = request.user.username
	if request.POST.get('b5m_charcoal') == 'on':
		b1_obj.b5m_charcoal = True
	else:
		b1_obj.b5m_charcoal = False

	if request.POST.get('b5m_kerosene') == 'on':
		b1_obj.b5m_kerosene = True
	else:
		b1_obj.b5m_kerosene = False

	if request.POST.get('b5m_wood') == 'on':
		b1_obj.b5m_wood = True
	else:
		b1_obj.b5m_wood = False

	if request.POST.get('b5m_gas') == 'on':
		b1_obj.b5m_gas = True
	else:
		b1_obj.b5m_gas = False

	if request.POST.get('b5m_electric') == 'on':
		b1_obj.b5m_electric = True
	else:
		b1_obj.b5m_electric = False

	 
	if request.POST.get('b5m_ac') == 'on':
		b1_obj.b5m_ac = True
	else:
		b1_obj.b5m_ac = False

	b1_obj.b5m_other_cooking_fuel = request.POST.get('b5m_other_cooking_fuel')
	b1_obj.b5m_exhaust = request.POST.get('b5m_exhaust')
	b1_obj.b5m_pesticide = request.POST.get('b5m_pesticide')
	b1_obj.b5m_garbage_burning = request.POST.get('b5m_garbage_burning')
	b1_obj.b5m_pet = request.POST.get('b5m_pet')
	b1_obj.b5m_pet_specify = request.POST.get('b5m_pet_specify')
	b1_obj.b5m_housing_type = request.POST.get('b5m_housing_type')
	b1_obj.b5m_landed_house_type = request.POST.get('b5m_landed_house_type')
	b1_obj.b5m_apartment_level_number = request.POST.get('b5m_apartment_level_number')
	b1_obj.b5m_dampness_house = request.POST.get('b5m_dampness_house')
	
	
	if request.POST.get('b5m_fan') == 'on':
		b1_obj.b5m_fan = True
	else:
		b1_obj.b5m_fan = False

	if request.POST.get('b5m_air_filter') == 'on':
		b1_obj.b5m_air_filter = True
	else:
		b1_obj.b5m_air_filter = False

	b1_obj.b5m_staying_out_history = request.POST.get('b5m_staying_out_history')
	b1_obj.b5m_staying_out_1st_street = request.POST.get('b5m_staying_out_1st_street')
	b1_obj.b5m_staying_out_1st_rt = request.POST.get('b5m_staying_out_1st_rt')
	b1_obj.b5m_staying_out_1st_rw = request.POST.get('b5m_staying_out_1st_rw')
	b1_obj.b5m_staying_out_1st_district = request.POST.get('b5m_staying_out_1st_district')
	b1_obj.b5m_staying_out_1st_city = request.POST.get('b5m_staying_out_1st_city')
	b1_obj.b5m_staying_out_1st_zipcode = request.POST.get('b5m_staying_out_1st_zipcode')
	b1_obj.b5m_staying_out_1st_duration = request.POST.get('b5m_staying_out_1st_duration')
	b1_obj.b5m_staying_out_2nd_street = request.POST.get('b5m_staying_out_2nd_street')
	b1_obj.b5m_staying_out_2nd_rt = request.POST.get('b5m_staying_out_2nd_rt')
	b1_obj.b5m_staying_out_2nd_rw = request.POST.get('b5m_staying_out_2nd_rw')
	b1_obj.b5m_staying_out_2nd_district = request.POST.get('b5m_staying_out_2nd_district')
	b1_obj.b5m_staying_out_2nd_city = request.POST.get('b5m_staying_out_2nd_city')
	b1_obj.b5m_staying_out_2nd_zipcode = request.POST.get('b5m_staying_out_2nd_zipcode')
	b1_obj.b5m_staying_out_2nd_duration = request.POST.get('b5m_staying_out_2nd_duration')
	b1_obj.b5m_notes = request.POST.get('b5m_notes')
	b1_obj.save()
	return b1_obj

@login_required(login_url='core:login')
def process_sectionB2F(request, participant_id, form_id):
	
	b1_form_obj = B2Pregnancy.objects.get(id=int(form_id))
	try:
		b1_obj = B2GestationalNutrition.objects.get(b1_form=b1_form_obj)
		print "masuk ke update_section1"
		return update_sectionB2F(request, participant_id, form_id)	
	except:
		print "masuk ke create_section1"
		return create_sectionB2F(request, participant_id, form_id)

@login_required(login_url='core:login')
def create_sectionB2F(request, participant_id, form_id):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		b1_form_obj = B2Pregnancy.objects.get(id=int(form_id))
		b1_obj = B2GestationalNutrition()
		b1_obj.b1_form = b1_form_obj
		b1_obj.participant_id = b1_form_obj.participant.participant_id
		b1_obj.data_entry_id = request.user.username
		b1_obj.created_time = datetime.datetime.now()
		b1_obj = save_sectionB2F(b1_obj, request, participant_id, form_id)
		print "masuk ke show section true"
		return show_sectionB2F(request, participant_id, form_id, True)	
	else:
		print "masuk ke show section false"
		return show_sectionB2F(request, participant_id, form_id, False)

@login_required(login_url='core:login')
def update_sectionB2F(request, participant_id, form_id):
	if request.method == "POST" and request.POST.get('context') == "SAVE":
		b1_obj = B2GestationalNutrition.objects.get(b1_form_id=int(form_id))
		b1_obj = save_sectionB2F(b1_obj, request, participant_id, form_id)
		print "masuk ke show section yang diupdate true"
		return show_sectionB2F(request, participant_id, form_id, True)	
	else:
		print "masuk ke show section1 yang diupdate false"
		return show_sectionB2F(request, participant_id, form_id, False)

@login_required(login_url='core:login')
def show_sectionB2F(request, participant_id, form_id, is_save):
	form = B2Pregnancy.objects.get(id=int(form_id))
	participant = Participant.objects.get(id=int(participant_id))
	interviewer = User.objects.get(id=form.interviewer_id)
	is_save_all = form.is_save_all	
	date_interviewed = form.date_interviewed
	date_data_entered = form.date_data_entered
	date_admission = form.date_admission
	role = ''
	if not request.user.is_staff:
		role = 'staff'
	try:
		b1_obj = B2GestationalNutrition.objects.get(b1_form_id=form.id) 			
		if form.date_data_checked is not None:
			date_data_checked = form.date_data_checked
			if is_save:
				return render(request, 'forms_b2/sectionB2F.html', {'success' : True, 'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj,  'date_data_checked' : date_data_checked})
			else:
				print 'b'
				return render(request, 'forms_b2/sectionB2F.html', {'participant' : participant,'date_data_checked' : date_data_checked, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj, 'date_data_checked' : date_data_checked})
		else:
			print 'c'
			if is_save:	
				print 'masuk ke yang is_save = true'
				return render(request, 'forms_b2/sectionB2F.html', {'success' : True, 'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj })
			else:
				print 'masuk ke yang is_save = false'
				return render(request, 'forms_b2/sectionB2F.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'update', 'form' : form,'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission, 'b1' : b1_obj })	
	except:
		print "masuk ke except yang form B2"
		return render(request, 'forms_b2/sectionB2F.html', {'participant' : participant, 'is_save_all' : is_save_all ,'interviewer' : interviewer, 'role' : role, 'context' : 'create', 'form' : form, 'date_interviewed' : date_interviewed, 'date_data_entered' : date_data_entered, 'date_admission' : date_admission})

def save_sectionB2F(b1_obj, request, participant_id, form_id):
	b1_obj.b6m_fasting_pregnancy = request.POST.get('b6m_fasting_pregnancy')
	b1_obj.updated_time = datetime.datetime.now()
	b1_obj.data_updated_id = request.user.username

	if request.POST.get('b6m_ramadhan') == 'on':
		b1_obj.b6m_ramadhan = True
	else:
		b1_obj.b6m_ramadhan = False

	if request.POST.get('b6m_sunnah') == 'on':
		b1_obj.b6m_sunnah = True
	else:
		b1_obj.b6m_sunnah = False

	b1_obj.b6m_fasting_duration = request.POST.get('b6m_fasting_duration')
	b1_obj.b6m_energy = request.POST.get('b6m_energy')
	b1_obj.b6m_water = request.POST.get('b6m_water')
	b1_obj.b6m_protein = request.POST.get('b6m_protein')
	b1_obj.b6m_fat = request.POST.get('b6m_fat')
	b1_obj.b6m_carbohydrate = request.POST.get('b6m_carbohydrate')
	b1_obj.b6m_dietary_fiber = request.POST.get('b6m_dietary_fiber')
	b1_obj.b6m_unsaturated_fat = request.POST.get('b6m_unsaturated_fat')
	b1_obj.b6m_cholestrol = request.POST.get('b6m_cholestrol')
	b1_obj.b6m_vitA = request.POST.get('b6m_vitA')
	b1_obj.b6m_carotene = request.POST.get('b6m_carotene')
	b1_obj.b6m_vitE = request.POST.get('b6m_vitE')
	b1_obj.b6m_vitB1 = request.POST.get('b6m_vitB1')
	b1_obj.b6m_vitB2 = request.POST.get('b6m_vitB2')
	b1_obj.b6m_vitB6 = request.POST.get('b6m_vitB6')
	b1_obj.b6m_folicAcid = request.POST.get('b6m_folicAcid')
	b1_obj.b6m_vitC = request.POST.get('b6m_vitC')
	b1_obj.b6m_sodium = request.POST.get('b6m_sodium')
	b1_obj.b6m_potassium = request.POST.get('b6m_potassium')
	b1_obj.b6m_calcium = request.POST.get('b6m_calcium')
	b1_obj.b6m_magnesium = request.POST.get('b6m_magnesium')
	b1_obj.b6m_phosporus = request.POST.get('b6m_phosporus')
	b1_obj.b6m_iron = request.POST.get('b6m_iron')
	b1_obj.b6m_zinc = request.POST.get('b6m_zinc')
	b1_obj.b6m_tea = request.POST.get('b6m_tea')
	b1_obj.b6m_coffee = request.POST.get('b6m_coffee')
	b1_obj.b6m_alcohol = request.POST.get('b6m_alcohol')
	b1_obj.b6m_antibiotics = request.POST.get('b6m_antibiotics')
	b1_obj.b6m_antibiotics_specify = request.POST.get('b6m_antibiotics_specify')
	b1_obj.b6m_antibiotics_duration = request.POST.get('b6m_antibiotics_duration')
	b1_obj.b6m_analgesia = request.POST.get('b6m_analgesia')
	b1_obj.b6m_analgesia_specify = request.POST.get('b6m_analgesia_specify')
	b1_obj.b6m_analgesia_duration = request.POST.get('b6m_analgesia_duration')
	b1_obj.b6m_supplement = request.POST.get('b6m_supplement')
	b1_obj.b6m_supplement_specify = request.POST.get('b6m_supplement_specify')
	b1_obj.b6m_supplement_duration =  request.POST.get('b6m_supplement_duration')
	b1_obj.b6m_supplement_routine = request.POST.get('b6m_supplement_routine')
	b1_obj.b6m_herbs = request.POST.get('b6m_herbs')
	b1_obj.b6m_herbs_specify = request.POST.get('b6m_herbs_specify')
	b1_obj.b6m_herbs_routine = request.POST.get('b6m_herbs_routine')
	b1_obj.b6m_herbs_duration = request.POST.get('b6m_herbs_duration')
	b1_obj.b6m_other_med_exist = request.POST.get('b6m_other_med_exist')
	b1_obj.b6m_other_med = request.POST.get('b6m_other_med')
	b1_obj.b6m_other_med_routine = request.POST.get('b6m_other_med_routine')
	b1_obj.b6m_other_med_duration = request.POST.get('b6m_other_med_duration')
	b1_obj.b6m_notes = request.POST.get('b6m_notes')
	b1_obj.save()
	return b1_obj