from django import forms
from .models import Article, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# class ArticleForm(forms.ModelForm):

#     class Meta:
#         model = Article
#         # fields = '__all__'
#         fields = ('title', 'content',)
#         widgets = {
#             'title': forms.TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     'style': 'width: 100%',
#                     'placeholder': '제목을 입력하세요.' }
#             ),
#             'content': forms.CharField(widget=CKEditorUploadingWidget()),
#         }
#         labels = {
#             'title': '제목',
#             'user': '작성자',
#             'content': '내용',
#         }

class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields['title'].widget.attrs.update({
            'placeholder': '제목을 입력해주세요.',
            'class': 'form-control',
            'autofocus': True,
        })

    class Meta:
        model = Article
        fields = ['title', 'content']
        labels = {
            'content': '내용',
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ('article', 'user',)
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': '내용을 입력하세요.'
                }
            ),
        }
        labels = {
            'content': '내용',
        }
