from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Genre, Movie, Movie_Review, Rank
from .forms import RankForm, ReviewForm


# Create your views here.
@require_GET
def index(request):
    movies = Movie.objects.all()
    
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


def detail(request, movie_pk):
    
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.movie_id = movie_pk
            review.user = request.user
            review.save()
            return redirect('movies:detail', movie_pk)
    else:
        review_form = ReviewForm()
        reviews = Movie_Review.objects.filter(movie_id=movie_pk)
    
    movie = get_object_or_404(Movie, pk=movie_pk)
    rank = Rank.objects.filter(user=request.user, movie_id=movie_pk)
    rank_form = RankForm()
    context = {
        'movie': movie,
        'review_form': review_form,
        'reviews': reviews,
        'rank': rank,
        'rank_form': rank_form,
    }
    return render(request, 'movies/detail.html', context)


def update_review(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Movie_Review, pk=review_pk)
    reviews = Movie_Review.objects.filter(movie=movie)

    if request.method == 'POST':
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


def delete_review(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Movie_Review, pk=review_pk)
    if request.user == review.user and request.method == 'POST':
        review.delete()
    return redirect('movies:detail', movie.pk)


def rank_create(request, movie_pk):
    if request.method == 'POST':
        rank_form = RankForm(request.POST)
        if rank_form.is_valid():
            rank = rank_form.save(commit=False)
            rank.movie_id = movie_pk
            rank.user = request.user
            rank.save()
            return redirect('movies:detail', movie_pk)
    return redirect('accounts:login')


def rank_update(request, movie_pk, rating_pk):
    pass