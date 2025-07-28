
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_doctor = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'country', 'city']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
