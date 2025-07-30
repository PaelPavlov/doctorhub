from django.urls import path
from .views import create_article
from . import views

urlpatterns = [
    path('create/', create_article, name='create_article'),
    path('delete/<int:article_id>/', views.delete_article, name='delete_article'),
    path('edit/<int:article_id>/', views.edit_article, name='edit_article'),
]
