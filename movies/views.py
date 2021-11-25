from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.shortcuts import get_list_or_404, render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Genre, Movie, Movie_Review, Rank
from .forms import RankForm, ReviewForm
import random
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse
import json
import copy
from django.contrib.auth import get_user_model


# Create your views here.
def search(request):
    # qs = Movie.objects.all()
    qs = Movie.objects.get_queryset().order_by('id')
    q = request.GET.get('q', '')
    print(q)
    if q:
        qs = qs.filter(title__icontains=q)
    pagenator = Paginator(qs, 4)
    page_number = request.GET.get('page')
    qs = pagenator.get_page(page_number)
    context = {
        'movies': qs,
        'q': q,
        'search_page': True,
    }
    return render(request, 'movies/index.html', context)


def home(request):
    first_popular_movie =  Movie.objects.get_queryset().order_by('-popularity').first()
    popular_movies = Movie.objects.get_queryset().order_by('-popularity')[1:]
    first_latest_movie = Movie.objects.get_queryset().order_by('-release_date').first
    latest_movies = Movie.objects.get_queryset().order_by('-release_date')[1:]

    context = {
        'first_popular_movie': first_popular_movie,
        'popular_movies': popular_movies,
        'first_latest_movie': first_latest_movie,
        'latest_movies': latest_movies,
    }
    return render(request, 'home.html', context)


@require_GET
def index(request):
    movies = Movie.objects.all()
    pagenator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    movies = pagenator.get_page(page_number)

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

    random_genre = random.sample(genres, 1)[0]
    similar_movie = Movie.objects.filter(
        Q(genres = random_genre.id) &
        ~Q(id = movie_pk)
    ).order_by('?')[:4]

    context = {
        'movie': movie,
        'genres': genres,
        'review_form': review_form,
        'rank': rank,
        'rank_form': rank_form,
        'random_genre': random_genre,
        'similar_movie': similar_movie,
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


movies = []
next_movies = []

def worldcup_init(request):
    global paginator
    global movies
    round = int(request.GET.get('round'))
    movies = random.sample(list(Movie.objects.order_by('-popularity')), round)
    paginator = Paginator(movies, 2)
    last_page = len(movies) // 2
    next_movies.clear()

    context = {
        'movies': movies[:2],
        'init_page': 1,
        'last_page': last_page,
        'round': round,
    }
    return render(request, 'movies/worldcup.html', context)


def worldcup_next_round(request):
    global paginator
    global movies
    global next_movies

    page_number = int(request.GET.get('page'))
    last_page = len(movies) // 2
    movie_params = []

    if page_number > last_page:
        print('change round')
        seletedMoviePks = request.GET.get('seletedMoviePks')
        movie = get_object_or_404(Movie, pk=seletedMoviePks)
        next_movies.append(movie)
        movies = copy.deepcopy(next_movies)
        last_page = len(movies) // 2


        movie_params = movies[:2]
        print(movie_params)
        data = serializers.serialize('json', movie_params)

        next_movies.clear()

        data2 = {
            'last_page': last_page,
            'movies' : data,
        }
        data2 = json.dumps(data2)
        return HttpResponse(data2, content_type='application/json')

    else:
        
        movie_params = movies[(page_number-1)*2:((page_number-1)*2 + 2)]
        

        data = serializers.serialize('json', movie_params)

        seletedMoviePks = request.GET.get('seletedMoviePks')
        movie = get_object_or_404(Movie, pk=seletedMoviePks)
        next_movies.append(movie)

        return HttpResponse(data, content_type='application/json')


def worldcup_end(request):
    if request.user.is_authenticated:
        seletedMoviePks = request.GET.get('seletedMoviePks')
        totalRound = request.GET.get('totalRound')
        print('우승영화!!')

        movie = get_object_or_404(Movie, pk=seletedMoviePks)

        user = get_object_or_404(get_user_model(), username=request.user)
        user.recommended_movie.add(movie)
        context = {
            'movie': movie,
            'total_round': totalRound,
        }

        return render(request, 'movies/worldcup_end.html', context)

    return redirect('movies:worldcup_init')

def worldcup_select_round(request):

    return render(request, 'movies/worldcup_select_round.html')