from django.urls import path
from . import views

urlpatterns = [
    path('doctors/<int:doctor_id>/review/', views.add_review, name='add_review'),
    path('doctors/<int:doctor_id>/review/', views.add_review, name='add_review'),
    path('reviews/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),


]
