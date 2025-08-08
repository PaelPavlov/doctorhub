from django.urls import path
from .views import register, home, CustomLoginView, profile_by_id, edit_profile_by_id, CustomPasswordChangeView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('<int:user_id>/profile/', profile_by_id, name='profile'),
    path('<int:user_id>/edit/', edit_profile_by_id, name='edit_profile'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='password_change'),

]
