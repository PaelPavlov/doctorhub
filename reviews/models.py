from django.db import models
from django.conf import settings
from doctors.models import DoctorProfile

class Review(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} → {self.doctor.user.username} ({self.rating}⭐)'
