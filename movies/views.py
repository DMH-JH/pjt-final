from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Genre, Movie, Movie_Review, Rank
from .forms import RankForm, ReviewForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


@require_GET
def index(request):
    movies = Movie.objects.all()
    
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


@require_http_methods(['GET', 'POST'])
def detail(request, movie_pk):
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.movie_id = movie_pk
            review.user = request.user
            review.save()
            return redirect('movies:detail', movie_pk)
    else:
        review_form = ReviewForm()
    
    movie = get_object_or_404(Movie, pk=movie_pk)
    genres = get_list_or_404(Genre, movie=movie)
    rank = Rank.objects.filter(user=request.user, movie_id=movie_pk).first()
    rank_form = RankForm()
    context = {
        'movie': movie,
        'genres': genres,
        'review_form': review_form,
        'rank': rank,
        'rank_form': rank_form,
    }
    return render(request, 'movies/detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def update_review(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Movie_Review, pk=review_pk)
    reviews = Movie_Review.objects.filter(movie=movie)

    if request.user == review.user and request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.movie_id = movie_pk
            review.user = request.user
            review.save()
            return redirect('movies:detail', movie_pk)
    
    else:
        review_form = ReviewForm(instance=review)
    
    context = {
        'review_form': review_form,
        'movie': movie,
        'reviews': reviews,
    }
    return render(request, 'movies/detail.html', context)


@login_required
@require_POST
def delete_review(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Movie_Review, pk=review_pk)
    if request.user == review.user and request.method == 'POST':
        review.delete()
    return redirect('movies:detail', movie.pk)


@login_required
@require_POST
def create_rank(request, movie_pk):
    if request.method == 'POST':
        rank_form = RankForm(request.POST)
        if rank_form.is_valid():
            rank = rank_form.save(commit=False)
            rank.movie_id = movie_pk
            rank.user = request.user
            rank.save()
            return redirect('movies:detail', movie_pk)
    return redirect('accounts:login')


@login_required
@require_http_methods(['GET', 'POST'])
def update_rank(request, movie_pk, rank_pk):
    rank = get_object_or_404(Rank, pk=rank_pk)
    if request.user == rank.user and request.method == 'POST':
        rank_form = RankForm(request.POST, instance = rank)
        if rank_form.is_valid():
            rank = rank_form.save(commit = False)
            rank.movie_id = movie_pk
            rank.user = request.user
            rank.save()
            redirect('movies:detail', movie_pk)
    else:
        rank_form = RankForm(instance = rank)
    movie = Movie.objects.get(pk=movie_pk)
    context = {
        'rank_form': rank_form,
        'rank': rank,
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)


@login_required
@require_POST
def delete_rank(request, movie_pk, rank_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    rank = get_object_or_404(Rank, pk=rank_pk)
    if request.user == rank.user and request.method == 'POST':
        rank.delete()
    return redirect('movies:detail', movie.pk)