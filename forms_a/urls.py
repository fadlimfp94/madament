from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views, forms

app_name = 'forms_a'
urlpatterns = [
	url(r'^create/form', views.create_form, name='create_form'),
	url(r'^check/form', views.check_form, name='check_form'),
	url(r'^edit/form', views.edit_form, name='edit_form'),
	url(r'^save/form', views.save_form, name='save_form'),
	url(r'^process/section1', views.process_section1, name='process_section1'),
	url(r'^process/section2', views.process_section2, name='process_section2'),
	url(r'^process/section3', views.process_section3, name='process_section3'),
	url(r'^process/section4', views.process_section4, name='process_section4'),
	url(r'^process/section5', views.process_section5, name='process_section5'),
]