from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

app_name = 'forms_b2'
# urlpatterns = [
# 	url(r'^create/form', views.create_form, name='create_form'),
# 	url(r'^check/form', views.check_form, name='check_form'),
# 	url(r'^edit/form', views.edit_form, name='edit_form'),
# 	url(r'^save/form', views.save_form, name='save_form'),
# 	url(r'^process/sectionB1A', views.process_sectionB1A, name='process_sectionB1A'),
# 	url(r'^process/sectionB1B', views.process_sectionB1B, name='process_sectionB1B'),
# 	url(r'^process/sectionB1C', views.process_sectionB1C, name='process_sectionB1C'),
# 	url(r'^process/sectionB1D', views.process_sectionB1D, name='process_sectionB1D'),
# 	url(r'^process/sectionB1E', views.process_sectionB1E, name='process_sectionB1E'),
# 	url(r'^process/sectionB1F', views.process_sectionB1F, name='process_sectionB1F'),
# ]


urlpatterns = [
	url(r'^create$', views.create_form, name='create_form'),

	url(r'^(?P<form_id>[0-9]+)/check$', views.check_form, name='check_form'),
	url(r'^(?P<form_id>[0-9]+)/edit$', views.edit_form, name='edit_form'),
	url(r'^(?P<form_id>[0-9]+)/save$', views.save_form, name='save_form'),
	
	url(r'^(?P<form_id>[0-9]+)$', views.process_form, name='process_form'),
	url(r'^(?P<form_id>[0-9]+)/sectionB2A$', views.process_sectionB2A, name='process_sectionB2A'),
	url(r'^(?P<form_id>[0-9]+)/sectionB2B$', views.process_sectionB2B, name='process_sectionB2B'),
	url(r'^(?P<form_id>[0-9]+)/sectionB2C$', views.process_sectionB2C, name='process_sectionB2C'),
	url(r'^(?P<form_id>[0-9]+)/sectionB2D$', views.process_sectionB2D, name='process_sectionB2D'),
	url(r'^(?P<form_id>[0-9]+)/sectionB2E$', views.process_sectionB2E, name='process_sectionB2E'),
	url(r'^(?P<form_id>[0-9]+)/sectionB2F$', views.process_sectionB2F, name='process_sectionB2F'),
]