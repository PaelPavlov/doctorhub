from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from .forms import AppointmentDateForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from doctors.models import DoctorProfile

def generate_time_slots(doctor, date):
    weekday = date.weekday()
    slots = []

    hours = doctor.working_hours.filter(day=weekday)
    for wh in hours:
        current = datetime.combine(date, wh.start_time)
        end = datetime.combine(date, wh.end_time)

        while current + timedelta(hours=1) <= end:
            slot_start = current.time()
            slot_end = (current + timedelta(hours=1)).time()
            slots.append((slot_start, slot_end))
            current += timedelta(hours=1)

    booked = Appointment.objects.filter(doctor=doctor, date=date).values_list('start_time', flat=True)
    return [(s, e) for (s, e) in slots if s not in booked]



@login_required
def appointments_home(request):
    return render(request, 'appointments_home.html')



@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    selected_date = None
    available_slots = []

    if request.method == 'POST':
        form = AppointmentDateForm(request.POST)
        selected_slot = request.POST.get('slot')

        if form.is_valid():
            selected_date = form.cleaned_data['date']
            available_slots = generate_time_slots(doctor, selected_date)

            if selected_slot:
                start = datetime.strptime(selected_slot, '%H:%M').time()
                end = (datetime.combine(datetime.today(), start) + timedelta(hours=1)).time()

                Appointment.objects.create(
                    patient=request.user,
                    doctor=doctor,
                    date=selected_date,
                    start_time=start,
                    end_time=end
                )
                messages.success(request, "Appointment booked.")
                return redirect('user_dashboard')
    else:
        form = AppointmentDateForm()

    return render(request, 'book.html', {
        'form': form,
        'doctor': doctor,
        'slots': available_slots,
        'selected_date': selected_date
    })


@login_required
def doctor_dashboard(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)

    today = now().date()

    upcoming_appointments = Appointment.objects.filter(
        doctor=doctor,
        date__gte=today,
        status='booked'
    ).order_by('date', 'start_time')

    working_hours = doctor.working_hours.order_by('day')

    return render(request, 'doctor_dashboard.html', {
        'doctor': doctor,
        'appointments': upcoming_appointments,
        'working_hours': working_hours,
    })


@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user).order_by('-date')
    return render(request, 'my_appointments.html', {'appointments': appointments})

@login_required
def doctor_appointments(request):
    doctor_profile = getattr(request.user, 'doctor_profile', None)
    if not doctor_profile:
        return redirect('home')
    appointments = Appointment.objects.filter(doctor=doctor_profile).order_by('-date')
    return render(request, 'doctor_appointments.html', {'appointments': appointments})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user != appointment.patient and getattr(request.user, 'doctor_profile', None) != appointment.doctor:
        return HttpResponseForbidden()

    appointment.status = 'cancelled'
    appointment.save()
    messages.success(request, "Appointment cancelled successfully.")
    return redirect(request.META.get('HTTP_REFERER', 'appointments_home'))


@login_required
def user_dashboard(request):
    today = now().date()

    upcoming_appointments = Appointment.objects.filter(
        patient=request.user,
        date__gte=today,
        status='booked'
    ).order_by('date', 'start_time')

    past_appointments = Appointment.objects.filter(
        patient=request.user,
        date__lt=today
    ).order_by('-date', '-start_time')

    return render(request, 'user_dashboard.html', {
        'appointments': upcoming_appointments,
        'past_appointments': past_appointments,
    })
