from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from articles.models import Article
from .forms import CustomUserCreationForm, CustomLoginForm, UserUpdateForm, CustomPasswordChangeForm
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render



def home(request):
    articles = Article.objects.all()

    is_staffadmin = False
    if request.user.is_authenticated:
        is_staffadmin = request.user.groups.filter(name='StaffAdmins').exists()

    return render(request, 'home.html', {
        'articles': articles,
        'is_staffadmin': is_staffadmin,
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomLoginForm

    def form_valid(self, form):
        remember = self.request.POST.get('remember_me')
        if not remember:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(1209600)
        return super().form_valid(form)


def about(request):
    return render(request, 'about.html')

@login_required
def profile_by_id(request, user_id):
    profile_user = get_object_or_404(CustomUser, id=user_id)

    if request.user != profile_user:
        return redirect('profile', user_id=request.user.id)

    return render(request, 'profile.html', {'profile_user': profile_user})


@login_required
def edit_profile_by_id(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.user != user:
        return redirect('home')

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user.id)
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'password_change.html'
    success_url = reverse_lazy('home')
