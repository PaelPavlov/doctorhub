from django.contrib import admin
from .models import DoctorProfile, WorkingHour

class WorkingHourInline(admin.TabularInline):
    model = WorkingHour
    extra = 0

class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'town', 'hospital_name')
    list_filter = ('specialty',)
    inlines = [WorkingHourInline]

admin.site.register(DoctorProfile, DoctorProfileAdmin)
