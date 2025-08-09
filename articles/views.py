from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm
from .models import Article


def is_staffadmin(user):
    return user.groups.filter(name='StaffAdmins').exists()

@login_required
@user_passes_test(is_staffadmin)
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.is_approved = False  #Not needed currently
            article.save()
            return redirect('home')
    else:
        form = ArticleForm()
    return render(request, 'articles/create_article.html', {'form': form})

@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.user == article.author or request.user.is_superuser:
        article.delete()
    return redirect('home')

@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.user != article.author and not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'articles/edit_article.html', {'form': form})