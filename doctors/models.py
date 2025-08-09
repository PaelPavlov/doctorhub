from django.db import models
from django.db.models import Avg

from users.models import CustomUser

DAY_CHOICES = [
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
]

class DoctorProfile(models.Model):
    SPECIALTY_CHOICES = [
        ('Orthopedist', 'Orthopedist'),
        ('Dentist', 'Dentist'),
        ('Family Doctor', 'Family Doctor'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    town = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=255)
    hospital_address = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES)
    profile_picture = models.ImageField(upload_to='doctor_pics/', blank=True, null=True)

    def average_rating(self):
        return self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} ({self.specialty})"


class WorkingHour(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='working_hours')
    day = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

