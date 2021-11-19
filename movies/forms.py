from django import forms
from .models import Movie_Review, Rank

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Movie_Review
        # fields = '__all__'
        exclude = ['movie', 'user']


class RankForm(forms.ModelForm):
    class Meta:
        model = Rank
        exclude = ['movie', 'user']