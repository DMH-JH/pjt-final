from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from movies.models import Movie

# Create your models here.
class User(AbstractUser):
    profile_img = ProcessedImageField(upload_to='images/',
                            processors=[ResizeToFill(400,400)],
                            format='JPEG',
                            options={'quality': 100}
                )
    recommended_movie = models.ManyToManyField(Movie)

