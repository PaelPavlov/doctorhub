from django.urls import path
from .views import doctor_register
from . import views

urlpatterns = [
    path('register/', doctor_register, name='doctor_register'),
    path('<int:doctor_id>/profile/', views.doctor_profile_view, name='doctor_profile'),
    path('<int:doctor_id>/edit/', views.edit_doctor_profile_view, name='edit_doctor_profile'),
    path('all/', views.doctor_list, name='doctor_list'),
    path('api/doctors/', views.api_doctor_list, name='api_doctor_list'),

]
