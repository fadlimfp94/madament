from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(B2Pregnancy)
admin.site.register(B2MedicalData)
admin.site.register(B2UltrasoundScanResults)
admin.site.register(B2CurrentSmookingHabits)
admin.site.register(B2PollutanExposure)
admin.site.register(B2GestationalNutrition)

