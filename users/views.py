from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from articles.models import Article
from .forms import CustomUserCreationForm, CustomLoginForm, UserUpdateForm
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import render



# def home(request):
#     articles = Article.objects.filter(is_approved=True).order_by('-created_at')[:5]
#     return render(request, 'home.html', {'articles': articles})


def home(request):
    articles = Article.objects.all()

    is_staffadmin = False
    if request.user.is_authenticated:
        is_staffadmin = request.user.groups.filter(name='StaffAdmins').exists()

    return render(request, 'home.html', {
        'articles': articles,
        'is_staffadmin': is_staffadmin,
    })
# def home(request):
#     return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect('login')
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
            self.request.session.set_expiry(1209600)  # 2 weeks
        return super().form_valid(form)




@login_required
def profile_by_id(request, user_id):
    user_obj = get_object_or_404(CustomUser, id=user_id)

    if request.user != user_obj:
        return redirect('profile', user_id=request.user.id)

    return render(request, 'profile.html', {'user': user_obj})

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