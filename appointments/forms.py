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
