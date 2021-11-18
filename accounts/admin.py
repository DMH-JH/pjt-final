from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User



'''
장고(django)의 관리자 페이지에서 사용하는 폼(Form)을 수정하기 위해 
자체적으로 커스텀 유저 모델(Custom User Model)에 맞는 Form을 생성
'''
# Register your models here.
admin.site.register(User, UserAdmin)
