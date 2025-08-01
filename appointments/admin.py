from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date', 'start_time', 'end_time', 'status')
    list_filter = ('doctor', 'status', 'date')
