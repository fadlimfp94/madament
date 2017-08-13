from django.conf.urls import include, url
from django.contrib.auth.views import login, logout
from . import views, forms

app_name = 'core'

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^participant/$', views.participant_list, name='participant_list'),
	url(r'^participant/create/$', views.create_participant, name='create_participant'),
	url(r'^participant/edit/(?P<participant_id>[0-9]+)/$', views.edit_participant, name='edit_participant'),
	url(r'^participant/(?P<participant_id>[0-9]+)/$', views.forms, name='forms'),

	## FADLI
	url(r'^participant/(?P<participant_id>[0-9]+)/form_a/$', views.form_a, name='form_a'),
	url(r'^participant/(?P<participant_id>[0-9]+)/form_a/', include('forms_a.urls')),
	url(r'^participant/(?P<participant_id>[0-9]+)/form_d/visit/(?P<visiting_id>[1-4])/$', views.form_d, name='form_d'),
	url(r'^participant/(?P<participant_id>[0-9]+)/form_d/visit/(?P<visiting_id>[1-4])/', include('forms_d.urls')),
	url(r'^participant/(?P<participant_id>[0-9]+)/form_d/visit/$', views.redirect_to_forms, name='form_d'),
	## GAMA
	#url(r'^participant/(?P<participant_id>[0-9])/form_b1/$', views.form_b1, name='form_b1'),
	#url(r'^participant/(?P<participant_id>[0-9])/form_b2/$', views.form_b2, name='form_b2'),
	#url(r'^participant/(?P<participant_id>[0-9])/form_b3/$', views.form_b3, name='form_b3'),
	#url(r'^participant/(?P<participant_id>[0-9])/form_c/$', views.form_c, name='form_c'),

	url(r'^login/$', login, {'template_name': 'login.html', 'authentication_form': forms.LoginForm}, name='login'),
    url(r'^logout/$', logout, {'next_page': 'core:login'}, name='logout'),	
]