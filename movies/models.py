from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)

class Movie(models.Model):
    genres = models.ManyToManyField(Genre)

    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    original_language = models.CharField(max_length=30)
    overview = models.TextField()
    release_date = models.DateTimeField()
    runtime = models.IntegerField()
    video_id = models.CharField(max_length=200)
    poster_path = models.CharField(max_length=300)
    popularity = models.FloatField()

# n번 유저가 m번 영화의 평점을 x점으로 매김
class Rank(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    rating = models.PositiveIntegerField()

class Movie_Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)