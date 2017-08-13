from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Puskesmas(models.Model):
	puskesmas_id = models.CharField(max_length=5)
	name = models.CharField(max_length=25)
	def __str__(self):
		return "[name : "+unicode(self.name)+"]"
		
class Participant(models.Model):
	participant_id = models.CharField(max_length=10)
	name = models.CharField(max_length=25)
	date_admission = models.CharField(max_length=15)
	puskesmas = models.ForeignKey(Puskesmas, on_delete=models.PROTECT)
	created_by = models.CharField(max_length=25)
	edited_by = models.CharField(max_length=25)
	def __str__(self):
		return "[name : "+unicode(self.name)+"]"

class Child(models.Model):
	child_id = models.CharField(max_length=12)
	name = models.CharField(max_length=25)
	mother = models.ForeignKey(Participant, on_delete=models.PROTECT)	
	def __str__(self):
		return "[name : "+unicode(self.name)+"]"