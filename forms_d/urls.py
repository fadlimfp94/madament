from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

app_name = 'forms_d'

urlpatterns = [
	url(r'^create$', views.create_form, name='create_form'),
	
	url(r'^(?P<form_id>[0-9]+)/check$', views.check_form, name='check_form'),
	url(r'^(?P<form_id>[0-9]+)/edit$', views.edit_form, name='edit_form'),
	url(r'^(?P<form_id>[0-9]+)/save$', views.save_form, name='save_form'),
	
	url(r'^(?P<form_id>[0-9]+)$', views.process_form, name='process_form'),
	url(r'^(?P<form_id>[0-9]+)/section1$', views.process_section1, name='process_section1'),
	url(r'^(?P<form_id>[0-9]+)/section2$', views.process_section2, name='process_section2'),
	url(r'^(?P<form_id>[0-9]+)/section3$', views.process_section3, name='process_section3'),
	url(r'^(?P<form_id>[0-9]+)/section4$', views.process_section4, name='process_section4'),
	url(r'^(?P<form_id>[0-9]+)/section5$', views.process_section5, name='process_section5'),
	url(r'^(?P<form_id>[0-9]+)/section6$', views.process_section6, name='process_section6'),
	url(r'^(?P<form_id>[0-9]+)/section7$', views.process_section7, name='process_section7'),
	url(r'^(?P<form_id>[0-9]+)/section8$', views.process_section8, name='process_section8'),
]