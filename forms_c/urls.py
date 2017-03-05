from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

app_name = 'forms_c'
urlpatterns = [
	url(r'^create/form', views.create_form, name='create_form'),
	url(r'^check/form', views.check_form, name='check_form'),
	url(r'^edit/form', views.edit_form, name='edit_form'),
	url(r'^save/form', views.save_form, name='save_form'),
	url(r'^process/sectionC1', views.process_sectionC1, name='process_sectionC1'),	
]


