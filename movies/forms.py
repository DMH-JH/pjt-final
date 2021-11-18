from django import forms
from .models import Movie_Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Movie_Review
        # fields = '__all__'
        exclude = ['movie', 'user']