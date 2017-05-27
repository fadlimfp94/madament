from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views, forms

app_name = 'core'

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^participant/$', views.participant_list, name='participant_list'),
	url(r'^participant/create/$', views.create_participant, name='create_participant'),
	url(r'^participant/(?P<participant_id>[0-9])/$', views.forms, name='forms'),

	## FADLI
	url(r'^participant/(?P<participant_id>[0-9])/form_a/$', views.form_a, name='form_a'),
	url(r'^participant/(?P<participant_id>[0-9])/form_d1/$', views.form_d1, name='form_d1'),
	url(r'^participant/(?P<participant_id>[0-9])/form_d2/$', views.form_d2, name='form_d2'),
	url(r'^participant/(?P<participant_id>[0-9])/form_d3/$', views.form_d3, name='form_d3'),
	url(r'^participant/(?P<participant_id>[0-9])/form_d4/$', views.form_d4, name='form_d4'),
	
	## GAMA
	#url(r'^participant/(?P<participant_id>[0-9])/form_b1/$', views.form_b1, name='form_b1'),
	#url(r'^participant/(?P<participant_id>[0-9])/form_b2/$', views.form_b2, name='form_b2'),
	#url(r'^participant/(?P<participant_id>[0-9])/form_b3/$', views.form_b3, name='form_b3'),
	#url(r'^participant/(?P<participant_id>[0-9])/form_c/$', views.form_c, name='form_c'),

	url(r'^login/$', login, {'template_name': 'login.html', 'authentication_form': forms.LoginForm}, name='login'),
    url(r'^logout/$', logout, {'next_page': 'core:login'}, name='logout'),	
]