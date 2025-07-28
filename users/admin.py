from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_doctor', 'is_staff', 'is_superuser')
    list_filter = ('is_doctor', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('country', 'city', 'street', 'telephone', 'profile_picture', 'is_doctor')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('country', 'city', 'street', 'telephone', 'is_doctor')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
