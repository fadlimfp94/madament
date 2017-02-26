from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views, forms

app_name = 'core'

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^participant/create', views.create_participant, name='create_participant'),
	url(r'^participant/forms', views.forms, name='forms'),
	url(r'^participant/form_a', views.form_a, name='form_a'),
	url(r'^login/$', login, {'template_name': 'login.html', 'authentication_form': forms.LoginForm}, name='login'),
    url(r'^logout/$', logout, {'next_page': 'core:login'}, name='logout'),	
]