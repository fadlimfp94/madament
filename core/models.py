from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Puskesmas(models.Model):
	puskesmas_id = models.CharField(max_length=5, blank=True)
	name = models.CharField(max_length=25, blank=True)
	def __str__(self):
		return "[puskesmas_id : " + unicode(self.puskesmas_id)+ ", name : "+unicode(self.name)+"]"
		
class Participant(models.Model):
	participant_id = models.CharField(max_length=10, blank=True)
	name = models.CharField(max_length=30, blank=True)
	date_admission = models.DateField()
	puskesmas = models.ForeignKey(Puskesmas, on_delete=models.PROTECT)
	created_by = models.CharField(max_length=25, blank=True)
	updated_by = models.CharField(max_length=25, blank=True)
	created_time = models.CharField(max_length=50, blank=True)
	updated_time = models.CharField(max_length=50, blank=True)
	active_status = models.BooleanField(default=True)
	def __str__(self):
		return "[participant_id : " + unicode(self.participant_id)+ ", name : "+unicode(self.name)+ ", active_status : "+unicode(self.active_status)+"]"

class Child(models.Model):
	child_id = models.CharField(max_length=12, blank=True)
	name = models.CharField(max_length=30, blank=True)
	mother = models.ForeignKey(Participant, on_delete=models.PROTECT)	
	def __str__(self):
		return "[mother name : " + unicode(self.mother.name)+ ", child name : "+unicode(self.name)+"]"