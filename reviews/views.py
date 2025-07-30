from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from doctors.models import DoctorProfile
from django.core.exceptions import PermissionDenied
from .forms import ReviewForm
from .models import Review
from rest_framework import viewsets, permissions
from .serializers import ReviewSerializer


def is_staff_admin(user):
    return user.groups.filter(name='StaffAdmins').exists()

@login_required
def add_review(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)

    # Prevent duplicate reviews
    if Review.objects.filter(user=request.user, doctor=doctor).exists():
        return redirect('doctor_profile', doctor_id=doctor.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.doctor = doctor
            review.save()
            return redirect('doctor_profile', doctor_id=doctor.id)
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form, 'doctor': doctor})

from django.contrib import messages
from django.http import HttpResponseForbidden

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # if review.user != request.user:
    #     return HttpResponseForbidden("You can't edit someone else's review.")

    if not (
        request.user == review.user or
        request.user.is_superuser or
        is_staff_admin(request.user)
    ):
        raise PermissionDenied()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated successfully.")
            return redirect('doctor_profile', doctor_id=review.doctor.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'edit_review.html', {'form': form, 'doctor': review.doctor})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # if review.user != request.user:
    #     return HttpResponseForbidden("You can't delete someone else's review.")

    if not (
        request.user == review.user or
        request.user.is_superuser or
        is_staff_admin(request.user)
    ):
        raise PermissionDenied()

    doctor_id = review.doctor.id
    review.delete()
    messages.success(request, "Review deleted successfully.")
    return redirect('doctor_profile', doctor_id=doctor_id)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

def get_queryset(self):
    queryset = super().get_queryset()
    doctor_id = self.request.query_params.get('doctor')
    if doctor_id:
        queryset = queryset.filter(doctor_id=doctor_id)
    return queryset
