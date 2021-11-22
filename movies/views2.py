from django.shortcuts import render, redirect, get_object_or_404
from .models import  Movie, Rank
import random
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse

# def worldcup(request):
#     movies = random.sample(list(Movie.objects.order_by('-popularity'))[:50], 16)
#     paginator = Paginator(movies, 2)

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # /movies/?page=2 ajax 요청 => json
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         data = serializers.serialize('json', page_obj)
#         return HttpResponse(data, content_type='application/json')
#     # /movies/ 첫번째 페이지 요청 => html
#     else:
#         context = {
#             'movies': page_obj,
#         }
#         return render(request, 'movies/worldcup.html', context)


movies = random.sample(list(Movie.objects.order_by('-popularity'))[:50], 16)
paginator = Paginator(movies, 2)
# page = Paginator.page(paginator, 2)
next_movies = []

def worldcup(request):
    page_number = request.GET.get('page')
    # convert = page_number.content

    # print(page.next_page_number())
    print(type(page_number))
    print(type(paginator.num_pages))
    # if int(page_number) > paginator.num_pages:
    #     print('next_stage')

    page_obj = paginator.get_page(page_number)
    print(paginator.num_pages)
    # /movies/?page=2 ajax 요청 => json
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = serializers.serialize('json', page_obj)
        print(page_number)
        seletedMoviePks = request.GET.get('seletedMoviePks')
        next_movies.append(seletedMoviePks)
        print(next_movies)
        return HttpResponse(data, content_type='application/json')

    # /movies/ 첫번째 페이지 요청 => html
    else:
        context = {
            'movies': page_obj,
        }
        return render(request, 'movies/worldcup2.html', context)