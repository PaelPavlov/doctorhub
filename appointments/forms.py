from django import forms
from .models import Appointment
from django.utils import timezone

# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ['date', 'start_time', 'end_time']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#         }
#
#     def clean(self):
#         cleaned_data = super().clean()
#         start = cleaned_data.get('start_time')
#         end = cleaned_data.get('end_time')
#         if start and end and start >= end:
#             raise forms.ValidationError("End time must be after start time.")
#         return cleaned_data

from django import forms

class AppointmentDateForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Select a date'
    )


class SlotBookingForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Select a Date'
    )
    slot = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Select a Time Slot'
    )

    def __init__(self, *args, **kwargs):
        slots = kwargs.pop('slots', [])
        super().__init__(*args, **kwargs)
        self.fields['slot'].choices = [(s, s) for s in slots]
