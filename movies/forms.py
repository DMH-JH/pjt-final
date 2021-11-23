from django import forms
from .models import Movie_Review, Rank
from .widgets import starWidget

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Movie_Review
        # fields = ['content']
        exclude = ['movie', 'user']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': '내용을 입력하세요.'
                }
            ),
        }
        labels = {
            'content': '내용',
        }


class RankForm(forms.ModelForm):
    class Meta:
        model = Rank
        exclude = ['movie', 'user']
        widgets = {
            'rating': starWidget,
        }