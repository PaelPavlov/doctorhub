from django.urls import path
from .views import register, home, CustomLoginView, profile_by_id, edit_profile_by_id
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('<int:user_id>/profile/', profile_by_id, name='profile'),
    path('<int:user_id>/edit/', edit_profile_by_id, name='edit_profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name='password_change_done'),

]
