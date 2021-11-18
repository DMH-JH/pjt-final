from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Genre, Movie, Movie_Review
from .forms import ReviewForm


# Create your views here.
@require_GET
def index(request):
    movies = Movie.objects.all()
    
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)

@require_GET
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review_from = ReviewForm()
    reviews = movie.movie_review_set.all()
    
    context = {
        'movie': movie,
        'review_form': review_from,
        'reviews': reviews,
    }
    return render(request, 'movies/detail.html', context)


def create_review(request, movie_pk):
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
            
    context = {
        'review_form': review_form,
        'reviews': reviews,
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
