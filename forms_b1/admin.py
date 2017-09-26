from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(B1Pregnancy)
admin.site.register(B1MedicalData)
admin.site.register(B1UltrasoundScanResults)
admin.site.register(B1LaboratoryTest)
admin.site.register(B1CurrentSmookingHabits)
admin.site.register(B1PollutanExposure)
admin.site.register(B1GestationalNutrition)

