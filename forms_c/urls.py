from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

app_name = 'forms_c'
urlpatterns = [
	url(r'^create$', views.create_form, name='create_form'),
	url(r'^(?P<form_id>[0-9]+)/check$', views.check_form, name='check_form'),
	url(r'^(?P<form_id>[0-9]+)/edit$', views.edit_form, name='edit_form'),
	url(r'^(?P<form_id>[0-9]+)/save$', views.save_form, name='save_form'),
	
	url(r'^(?P<form_id>[0-9]+)$', views.process_form, name='process_form'),

	url(r'^(?P<form_id>[0-9]+)/section1$', views.process_sectionC1, name='process_sectionC1'),
	url(r'^(?P<form_id>[0-9]+)/section2$', views.process_sectionC2, name='process_sectionC2'),
	url(r'^(?P<form_id>[0-9]+)/section3$', views.process_sectionC3, name='process_sectionC3'),
]




