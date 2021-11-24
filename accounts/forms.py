from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import widgets

'''
장고(django)의 관리자 페이지에서 사용하는 폼(Form)을 수정하기 위해 
자체적으로 커스텀 유저 모델(Custom User Model)에 맞는 Form을 생성
'''
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('profile_img',)
        labels = {
            'profile_img': '프로필 사진'
        }

