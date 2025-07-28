from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor', 'rating', 'created_at')
    search_fields = ('user__username', 'doctor__user__username')
