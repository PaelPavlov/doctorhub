from django.urls import path
from . import views


urlpatterns = [
    path('', views.appointments_home, name='appointments_home'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('my/', views.my_appointments, name='my_appointments'),
    path('doctor/', views.doctor_appointments, name='doctor_appointments'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),

]

