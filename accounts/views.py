from django.contrib.auth.models import User
from django.http import request
from django.shortcuts import get_list_or_404, redirect, render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST

from community.models import Comment, Article
from movies.models import Rank, Movie
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.db.models import Sum

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form':form,
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'home')
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('community:index')
        

def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    ranks = Rank.objects.filter(user=person).values('movie_id')
    ranks = [r['movie_id'] for r in ranks]
    runtime_total = 0
    for r in ranks:
        runtime_total += Movie.objects.get(id=r).runtime
    distincts = Comment.objects.filter(user=person).values('article_id').order_by('-article').distinct()
    articles = Article.objects.filter(id__in=[d['article_id'] for d in distincts])
    recommended_movies = person.recommended_movie.all()

    context = {
        'person': person,
        'ranks': ranks,
        'cmt_articles': articles,
        'runtime_total': runtime_total,
        'recommended_movies': recommended_movies,
    }
    return render(request, 'accounts/profile.html', context)
