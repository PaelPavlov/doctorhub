
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from users.forms import CustomUserCreationForm
from .forms import DoctorProfileForm, WorkingHourFormSet
from .models import WorkingHour
from .models import DoctorProfile
from .serializers import DoctorProfileSerializer





def doctor_register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = DoctorProfileForm(request.POST, request.FILES)
        formset = WorkingHourFormSet(request.POST)


        for name in list(user_form.fields):
            if name not in ['username', 'email', 'password1', 'password2']:
                del user_form.fields[name]

        if user_form.is_valid() and profile_form.is_valid() and formset.is_valid():

            user = user_form.save(commit=False)
            user.is_doctor = True
            user.save()

            doctor_profile = profile_form.save(commit=False)
            doctor_profile.user = user
            doctor_profile.save()

            working_hours = formset.save(commit=False)
            for wh in working_hours:
                wh.doctor = doctor_profile
                wh.save()

            login(request, user)
            return redirect('doctor_profile', doctor_id=doctor_profile.pk)
    else:
        user_form = CustomUserCreationForm()
        profile_form = DoctorProfileForm()
        formset = WorkingHourFormSet(queryset=WorkingHour.objects.none())

        for name in list(user_form.fields):
            if name not in ['username', 'email', 'password1', 'password2']:
                del user_form.fields[name]

    return render(request, 'doctor_register.html', {
        'form': user_form,
        'profile_form': profile_form,
        'formset': formset,
    })



def doctor_list(request):
    doctors = DoctorProfile.objects.prefetch_related('working_hours').filter(working_hours__isnull=False).distinct()

    town = request.GET.get('town')
    specialty = request.GET.get('specialty')

    if town:
        doctors = doctors.filter(town__icontains=town)

    if specialty:
        doctors = doctors.filter(specialty=specialty)

    doctors = doctors.order_by('specialty')

    paginator = Paginator(doctors, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'doctor_list.html', {
        'page_obj': page_obj,
        'town': town,
        'specialty': specialty
    })

@login_required
def doctor_profile_view(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    working_hours = doctor.working_hours.all()
    reviews = doctor.reviews.order_by('-created_at')

    user_review_exists = False
    if request.user.is_authenticated:
        user_review_exists = doctor.reviews.filter(user=request.user).exists()

    return render(request, 'doctor_profile.html', {
        'doctor': doctor,
        'working_hours': working_hours,
        'user_review_exists': user_review_exists,
        'reviews': reviews,
    })


@login_required
def edit_doctor_profile_view(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)

    if doctor.user != request.user:
        return redirect('home')

    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_profile', doctor_id=doctor.id)
    else:
        form = DoctorProfileForm(instance=doctor)

    return render(request, 'edit_doctor_profile.html', {'form': form, 'doctor': doctor})

@api_view(['GET', 'POST'])
def api_doctor_list(request):
    if request.method == 'GET':
        doctors = DoctorProfile.objects.all()
        serializer = DoctorProfileSerializer(doctors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DoctorProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_doctor_detail(request, doctor_id):
    try:
        doctor = DoctorProfile.objects.get(id=doctor_id)
    except DoctorProfile.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DoctorProfileSerializer(doctor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DoctorProfileSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = DoctorProfileSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
