from django.contrib import admin
from .models import Movie, Rank
from .forms import RankForm

# Register your models here.
admin.site.register(Movie)
# admin.site.register(Rank)

@admin.register(Rank)
class RankAmin(admin.ModelAdmin):
    form = RankForm