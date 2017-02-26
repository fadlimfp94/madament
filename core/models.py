from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Puskesmas(models.Model):
	puskesmas_id = models.CharField(max_length=5)
	name = models.CharField(max_length=25)

class Participant(models.Model):
	participant_id = models.CharField(max_length=10)
	name = models.CharField(max_length=25)
	date_admission = models.DateField()
	puskesmas = models.ForeignKey(Puskesmas, on_delete=models.PROTECT)