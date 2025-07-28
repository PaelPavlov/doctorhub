from django import forms
from django.forms import modelformset_factory

from users.models import CustomUser
from .models import DoctorProfile


from django.contrib.auth.forms import UserCreationForm

class DoctorUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        exclude = ['user']
        widgets = {
            'specialty': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

from django import forms
from .models import WorkingHour

class WorkingHourForm(forms.ModelForm):
    class Meta:
        model = WorkingHour
        exclude = ['doctor']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'step': 3600,
                    'min': '08:00',
                    'max': '17:00'
                }
            ),
            'end_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'step': 3600,
                    'min': '08:00',
                    'max': '17:00'
                }
            ),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing_class = field.widget.attrs.get('class', '')
            if 'form-control' not in existing_class and 'form-select' not in existing_class:
                field.widget.attrs['class'] = (existing_class + ' form-control').strip()



WorkingHourFormSet = modelformset_factory(
    WorkingHour,
    form=WorkingHourForm,
    extra=7,
    can_delete=True
)