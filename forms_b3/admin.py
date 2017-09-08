from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(B3Pregnancy)
admin.site.register(B3MedicalData)
admin.site.register(B3UltrasoundScanResults)
admin.site.register(B3CurrentSmookingHabits)
admin.site.register(B3PollutanExposure)
admin.site.register(B3GestationalNutrition)

