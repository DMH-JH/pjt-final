from django.forms.widgets import DateTimeBaseInput
from django.shortcuts import render, redirect, get_object_or_404
from .models import  Movie, Rank
import random
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse
import json
import copy
from django.template import loader

# movies = random.sample(list(Movie.objects.order_by('-popularity'))[:50], 16)
# paginator = Paginator(movies, 2)
# next_movies = []

# def worldcup_init(request):
#     global paginator
#     global movies
#     movies = random.sample(list(Movie.objects.order_by('-popularity'))[:50], 16)
#     next_movies.clear()
    # paginator = Paginator(movies, 2)

#     page_number = request.GET.get('page')

#     page_obj = paginator.get_page(1)
#     # print(paginator.num_pages)

#     context = {
#         'movies': page_obj,
#         'init_page': 1,
#         'last_page': paginator.num_pages,
#     }
#     return render(request, 'movies/worldcup2.html', context)


# def worldcup_next_round(request):
#     global paginator
#     global movies
#     page_number = request.GET.get('page')
#     paginator2 = ''

#     if int(page_number) > paginator.num_pages:
#         seletedMoviePks = request.GET.get('seletedMoviePks')
#         movie = get_object_or_404(Movie, pk=seletedMoviePks)
#         next_movies.append(movie)
       

#         paginator = Paginator(next_movies, 2)

#         page_obj = paginator.get_page(1)
#         data = serializers.serialize('json', page_obj)
#         print(paginator.num_pages)
#         print(next_movies)
#         movies = next_movies
#         # print(data)

#         print('last_stage')

#         test_data = {
#             'last_page': paginator.num_pages,
#             'movies' : data,
#         }
#         data2 = json.dumps(test_data)
#         next_movies.clear()
#         return HttpResponse(data2, content_type='application/json')

#     else:
#         print('next page')
#         print(paginator.object_list)
#         page_obj = paginator.get_page(page_number)
#         data = serializers.serialize('json', page_obj)

#         seletedMoviePks = request.GET.get('seletedMoviePks')
#         movie = get_object_or_404(Movie, pk=seletedMoviePks)
#         next_movies.append(movie)
#         # print(page_obj)
#         # print(data)


#         # print(data2)
#         return HttpResponse(data, content_type='application/json')



movies = []
next_movies = []

def worldcup_init(request):
    global paginator
    global movies
    movies = list(Movie.objects.order_by('-popularity'))[:4]
    paginator = Paginator(movies, 2)
    last_page = len(movies) // 2
    next_movies.clear()
    print(movies)

    context = {
        'movies': movies[:2],
        'init_page': 1,
        'last_page': last_page,
    }
    return render(request, 'movies/worldcup2.html', context)


def worldcup_next_round(request):
    global paginator
    global movies
    global next_movies

    page_number = int(request.GET.get('page'))
    last_page = len(movies) // 2
    movie_params = []
    # print(page_number, last_page)
    # print(movies)

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
    seletedMoviePks = request.GET.get('seletedMoviePks')
    totalRound = request.GET.get('totalRound')
    print('우승영화!!')

    movie = get_object_or_404(Movie, pk=seletedMoviePks)

    context = {
        'movie': movie,
        'total_round': totalRound,
    }

    # template = loader.get_template('movies/worldcup_end.html')
    # return HttpResponse(template.render(context, request))
    return render(request, 'movies/worldcup_end.html', context)
